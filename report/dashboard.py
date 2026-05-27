from typing import Any
import builtins

builtins.Any = Any

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

from fasthtml.common import *

from employee_events import Employee, Team
from utils import load_model

from base_components.base_component import BaseComponent
from base_components.dropdown import Dropdown
from base_components.radio import Radio
from base_components.data_table import DataTable
from base_components.matplotlib_viz import MatplotlibViz

from combined_components.form_group import FormGroup
from combined_components.combined_component import CombinedComponent


class DashboardHeader(BaseComponent):
    """
    Header for the employee or team dashboard.
    """

    def build_component(self, entity_id, model):
        title = (
            "Desempeño del empleado"
            if model.name == "employee"
            else "Desempeño del equipo"
        )

        return Div(
            H1(title),
            P(
                "Panel de control para supervisar productividad, eventos "
                "positivos/negativos y probabilidad estimada de reclutamiento."
            ),
            cls="dashboard-header",
        )


class EmployeeDropdown(Dropdown):
    """
    Dropdown listing all employees.
    """

    def component_data(self, entity_id, model):
        employees = model.names()
        return list(zip(employees["employee_name"], employees["employee_id"]))


class TeamDropdown(Dropdown):
    """
    Dropdown listing all teams.
    """

    def component_data(self, entity_id, model):
        teams = model.names()
        return list(zip(teams["team_name"], teams["team_id"]))


class EmployeeSelectorForm(FormGroup):
    """
    Form to select an employee.
    """

    id = "employee-selector-form"
    action = "/employee"
    method = "get"
    button_label = "Ver empleado"

    children = [
        EmployeeDropdown(
            id="employee-selector",
            name="entity_id",
            label="Selecciona empleado",
        )
    ]


class TeamSelectorForm(FormGroup):
    """
    Form to select a team.
    """

    id = "team-selector-form"
    action = "/team"
    method = "get"
    button_label = "Ver equipo"

    children = [
        TeamDropdown(
            id="team-selector",
            name="entity_id",
            label="Selecciona equipo",
        )
    ]


class SelectorPanel(BaseComponent):
    """
    Selector panel containing employee and team forms.
    """

    def build_component(self, entity_id, model):
        return Div(
            H2("Filtros"),
            P("Elige si quieres analizar un empleado individual o un equipo."),
            Radio(values=["Employee", "Team"], name="entity-type")(entity_id, model),
            Div(
                EmployeeSelectorForm()(entity_id, Employee()),
                TeamSelectorForm()(entity_id, Team()),
                cls="selector-forms",
            ),
            cls="selector-panel",
        )


class SummaryTable(DataTable):
    """
    Table showing aggregated model input data.
    """

    def component_data(self, entity_id, model):
        data = model.model_data(entity_id)
        return data.fillna(0)


class NotesTable(DataTable):
    """
    Table showing notes for the selected employee or team.
    """

    def component_data(self, entity_id, model):
        return model.notes(entity_id)


class RecruitmentRiskCard(BaseComponent):
    """
    Card showing predicted recruitment probability.
    """

    def build_component(self, entity_id, model):
        probability_text = "No disponible"

        try:
            ml_model = load_model()
            data = model.model_data(entity_id).fillna(0)

            if hasattr(ml_model, "predict_proba"):
                probabilities = ml_model.predict_proba(data)

                if probabilities.shape[1] > 1:
                    probability = probabilities[0][1]
                else:
                    probability = probabilities[0][0]

                probability_text = f"{probability:.2%}"

            elif hasattr(ml_model, "predict"):
                prediction = ml_model.predict(data)[0]
                probability_text = str(prediction)

        except Exception as error:
            probability_text = f"No disponible ({type(error).__name__})"

        return Div(
            H2("Probabilidad estimada de reclutamiento"),
            P(probability_text),
            cls="risk-card",
        )


class EventTrendChart(MatplotlibViz):
    """
    Line chart of positive and negative events over time.
    """

    def visualization(self, entity_id, model):
        data = model.event_counts(entity_id)

        if data.empty:
            plt.title("Sin datos de eventos")
            return

        data = data.copy()
        data["event_date"] = pd.to_datetime(data["event_date"])

        fig, ax = plt.subplots(figsize=(11, 5))

        ax.plot(
            data["event_date"],
            data["positive_events"],
            label="Eventos positivos",
            marker="o",
            linewidth=2,
            color="#2ca02c",
        )

        ax.plot(
            data["event_date"],
            data["negative_events"],
            label="Eventos negativos",
            marker="o",
            linewidth=2,
            color="#d62728",
        )

        ax.set_title("Tendencia de eventos positivos y negativos")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Número de eventos")

        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

        fig.autofmt_xdate(rotation=45)

        ax.legend()
        ax.grid(True, alpha=0.3)

        self.set_axis_styling(ax)


class EventBarChart(MatplotlibViz):
    """
    Bar chart comparing total positive and negative events.
    """

    def visualization(self, entity_id, model):
        data = model.event_counts(entity_id)

        if data.empty:
            plt.title("Sin datos de eventos")
            return

        positive_total = data["positive_events"].sum()
        negative_total = data["negative_events"].sum()

        fig, ax = plt.subplots(figsize=(8, 5))

        bars = ax.bar(
            ["Eventos positivos", "Eventos negativos"],
            [positive_total, negative_total],
            color=["#2ca02c", "#d62728"],
        )

        ax.set_title("Comparación total de eventos positivos y negativos")
        ax.set_xlabel("Tipo de evento")
        ax.set_ylabel("Total de eventos")
        ax.grid(axis="y", alpha=0.3)

        max_value = max(positive_total, negative_total)
        ax.set_ylim(0, max_value * 1.15)

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + max_value * 0.02,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=10,
                color="white",
            )

        plt.tight_layout()

        self.set_axis_styling(ax)


class DashboardPage(CombinedComponent):
    """
    Full dashboard page.
    """

    children = [
        DashboardHeader(),
        SelectorPanel(),
        RecruitmentRiskCard(),
        H2("Datos agregados para el modelo"),
        SummaryTable(),
        H2("Visualización 1: tendencia de eventos"),
        EventTrendChart(),
        H2("Visualización 2: comparación de eventos"),
        EventBarChart(),
        H2("Notas"),
        NotesTable(),
    ]


app, rt = fast_app()


@rt("/")
def get():
    """
    Default dashboard route.
    """
    return DashboardPage()("1", Employee())


@rt("/employee")
def get(entity_id: str = "1"):
    """
    Employee dashboard route.
    """
    return DashboardPage()(entity_id, Employee())


@rt("/team")
def get(entity_id: str = "1"):
    """
    Team dashboard route.
    """
    return DashboardPage()(entity_id, Team())


if __name__ == "__main__":
    serve()
