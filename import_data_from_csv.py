import click
import json

from gn_module_monitoring.monitoring.models import (
    TMonitoringVisits,
    TMonitoringObservations,
)
from geonature.utils.env import DB as db


import datetime
import uuid
import csv

from unidecode import unidecode

from geonature.app import create_app
from geonature.core.gn_monitoring.models import TBaseSites
from pypnusershub.db.models import User
from apptax.taxonomie.models import Taxref
from geonature.core.gn_meta.models import TDatasets
from geonature.core.gn_commons.models import TModules
from gn_module_monitoring.monitoring.models import (
    TMonitoringVisits,
    TMonitoringObservations,
)


def get_data(file_name):
    data = []
    lines = 0
    with open(file_name, newline="") as file:
        dr = csv.DictReader(file)
        for row in dr:
            data.append(row)
            lines += 1
    print(str(lines) + " lines in file")
    return data


def parse_site(line):
    if "Jas Lacroix" in line["NOM SITE"]:
        line["NOM SITE"] = "Jas-la-croix"
    if "Val haute" in line["NOM SITE"]:
        line["NOM SITE"] = "Val Haute"
    if "Côte Belle" in line["NOM SITE"] or "Cote Belle" in line["NOM SITE"]:
        line["NOM SITE"] = "Cote belle"
    if "Béranne" in line["NOM SITE"]:
        line["NOM SITE"] = "Beranne"
    if "fournel bas" in line["NOM SITE"]:
        line["NOM SITE"] = "Fournel bas"
    if "Carmétran" in line["NOM SITE"]:
        line["NOM SITE"] = "Carmetran"
    if "combe guyon" in line["NOM SITE"]:
        line["NOM SITE"] = "Combe guyon"
    if "charges" in line["NOM SITE"]:
        line["NOM SITE"] = "Charges"
    if "Morgon" in line["NOM SITE"]:
        line["NOM SITE"] = "morgon"
    if "Mizoën" in line["NOM SITE"]:
        line["NOM SITE"] = "Mizoen"
    if "distroit" in line["NOM SITE"]:
        line["NOM SITE"] = "Distroit"
    if "Vallon valsenestre" in line["NOM SITE"]:
        line["NOM SITE"] = "Valsenestre"
    base_site_name = line["NOM SITE"] + "-" + line["NPOINT"]
    print(base_site_name)
    site = TBaseSites.query.filter_by(base_site_name=base_site_name).one_or_none()
    return site


def parse_observers(line):
    observers = []
    for key in ["OBSERVATEUR 1", "OBSERVATEUR 2"]:
        if line[key] != "":
            if " " in line[key]:
                name = line[key].split(" ")
                print(name)
                if len(name[1]) == 1:
                    obs = User.query.filter_by(nom_role=unidecode(name[0])).one()
                else:
                    try:
                        obs = (
                            User.query.filter_by(nom_role=unidecode(name[0]))
                            .filter_by(prenom_role=unidecode(name[1]))
                            .one()
                        )
                    except:
                        try:
                            obs = User.query.filter_by(
                                identifiant=(
                                    unidecode(name[1]).lower()
                                    + "."
                                    + unidecode(name[0]).lower()
                                )
                            ).one()
                        except:
                            obs = User.query.filter_by(
                                identifiant=(
                                    unidecode(name[0]).lower()
                                    + "."
                                    + unidecode(name[1]).lower()
                                )
                            ).one_or_none()
            elif "." in line[key]:
                surname = line[key].split(".")[-1]
                surname = surname.capitalize()
                obs = User.query.filter_by(nom_role=surname).one()
            elif " " not in line[key] and "." not in line[key]:
                surname = line[key]
                obs = User.query.filter_by(nom_role=surname).one()
            observers.append(obs)
    return observers


def parse_taxon(line):
    if (
        line["ESPECE"] is not None
        and "aucun" not in line["ESPECE"]
        and line["ESPECE"] != ""
        and line["ESPECE"] != "Néant"
        and line["ESPECE"] != "0"
    ):
        line["ESPECE"] = line["ESPECE"].capitalize()
        if "Merle a plastron" in line["ESPECE"]:
            line["ESPECE"] = "Merle à plastron"
        if "Rouge-gorge familier" in line["ESPECE"] or "Rouge gorge" in line["ESPECE"]:
            line["ESPECE"] = "Rougegorge familier"
        if (
            "Linotte Mélodieuse" in line["ESPECE"]
            or "Linotte melodieuse" in line["ESPECE"]
        ):
            line["ESPECE"] = "Linotte mélodieuse"
        if "Fauvette a tete noire" in line["ESPECE"]:
            line["ESPECE"] = "Fauvette à tête noire"
        if (
            "Hirondelle de rocher" in line["ESPECE"]
            or "Hirondelle des rochers" in line["ESPECE"]
        ):
            line["ESPECE"] = "Hirondelle de rochers"
        if "Hirondelle de fenetre" in line["ESPECE"]:
            line["ESPECE"] = "Hirondelle de fenêtre"
        if "Tarier patre" in line["ESPECE"]:
            line["ESPECE"] = "Tarier pâtre"
        if "Martinet alpin" in line["ESPECE"]:
            line["ESPECE"] = "Martinet à ventre blanc, Martinet alpin"
        if "Pic epeiche" in line["ESPECE"]:
            line["ESPECE"] = "Pic épeiche"
        if "Cassenoix mouchete" in line["ESPECE"]:
            line["ESPECE"] = "Cassenoix moucheté"
        if "Bec croisé des sapins" in line["ESPECE"]:
            line["ESPECE"] = "Bec-croisé des sapins"
        if (
            "Pie grièche ecorcheur" in line["ESPECE"]
            or "Pie grièche écorcheur" in line["ESPECE"]
        ):
            line["ESPECE"] = "Pie-grièche écorcheur"
        if "Roitelet triple bandeau" in line["ESPECE"]:
            line["ESPECE"] = "Roitelet à triple bandeau"
        if "Vanneau huppe" in line["ESPECE"]:
            line["ESPECE"] = "Vanneau huppé"
        if (
            "Rouge-queue noir" in line["ESPECE"]
            or "Rougequeue noir" in line["ESPECE"]
            or "Rouge queue noir" in line["ESPECE"]
        ):
            line["ESPECE"] = "Rougequeue noir"
        if (
            "Rouge-queue à front blanc" in line["ESPECE"]
            or "Rouge-queue a front blanc" in line["ESPECE"]
        ):
            line["ESPECE"] = "Rougequeue à front blanc"
        if "Pouillot de bonelli" in line["ESPECE"]:
            line["ESPECE"] = "Pouillot de Bonelli"
        if "Bergeronnette sp" in line["ESPECE"]:
            line["ESPECE"] = "Bergeronnette grise"
        if "Guépier d'europe" in line["ESPECE"]:
            line["ESPECE"] = "Guêpier d'Europe"
        if "Casse noix" in line["ESPECE"] or "Cassenoix moucheté" in line["ESPECE"]:
            line["ESPECE"] = "Cassenoix moucheté, Casse-noix"
        if (
            "Epervier d'europe" in line["ESPECE"]
            or "Epervier d'Europe" in line["ESPECE"]
        ):
            line["ESPECE"] = "Épervier d'Europe"
        if "Pipit des arbres" in line["ESPECE"]:
            line["ESPECE"] = "Pipit des arbres"
        if "Gypaete" in line["ESPECE"]:
            line["ESPECE"] = "Gypaète barbu"
        if "Heron cendre" in line["ESPECE"]:
            line["ESPECE"] = "Héron cendré"
        if (
            "Mésange charbonniere" in line["ESPECE"]
            or "Mesange charbonniere" in line["ESPECE"]
        ):
            line["ESPECE"] = "Mésange charbonnière"
        if "Mesange noire" in line["ESPECE"]:
            line["ESPECE"] = "Mésange noire"
        if "Chocard a bec jaune" in line["ESPECE"]:
            line["ESPECE"] = "Chocard à bec jaune"
        if "Crave a bec rouge" in line["ESPECE"]:
            line["ESPECE"] = "Crave à bec rouge"
        if (
            "Tarier des pres" in line["ESPECE"]
            or "Tarier des près" in line["ESPECE"]
            or "Tarier des prés" in line["ESPECE"]
        ):
            line["ESPECE"] = "Tarier des prés, Traquet tarier"
        if "Caille des bles" in line["ESPECE"]:
            line["ESPECE"] = "Caille des blés"
        if (
            "Faucon crecerelle" in line["ESPECE"]
            or "faucon crecerelle" in line["ESPECE"]
            or "faucon crécerelle" in line["ESPECE"]
        ):
            line["ESPECE"] = "Faucon crécerelle"
        if "Pouillot veloce" in line["ESPECE"]:
            line["ESPECE"] = "Pouillot véloce"
        if "Tetras lyre" in line["ESPECE"] or "Tetras-lyre" in line["ESPECE"]:
            line["ESPECE"] = "Tétras lyre"
        if "Lagopede alpin" in line["ESPECE"]:
            line["ESPECE"] = "Lagopède alpin"
        if "Sizerin flamme" in line["ESPECE"]:
            line["ESPECE"] = "Sizerin flammé"
        if "Geai des chenes" in line["ESPECE"]:
            line["ESPECE"] = "Geai des chênes"
        if "Monticole de roche" in line["ESPECE"]:
            line["ESPECE"] = "Monticole de roche, Merle de roche"
        if "Niverolle alpine" in line["ESPECE"]:
            line["ESPECE"] = "Niverolle alpine, Niverolle des Alpes"

        tax = (
            Taxref.query.filter(Taxref.cd_nom == Taxref.cd_ref)
            .filter(Taxref.nom_vern == line["ESPECE"])
            .first()
        )
        print(line["ESPECE"])
        return tax.cd_nom
    else:
        return -1


def parse_date(line):
    if "-" in line["DATE"]:
        date_tab = line["DATE"].split("-")
        date = datetime.date(int(date_tab[0]), int(date_tab[1]), int(date_tab[2]))
    elif "/" in line["DATE"]:
        date_tab = line["DATE"].split("/")
        if len(date_tab[2]) == 2:
            year = int(date_tab[2]) + 2000
        else:
            year = int(date_tab[2])
        day = int(date_tab[0])
        month = int(date_tab[1])
        if month > 12:
            day = int(date_tab[1])
            month = int(date_tab[0])
        date = datetime.date(year, month, day)
    return date


def parse_time(line):
    if line["HEURE DEBUT"][-1] == "h" or line["HEURE DEBUT"][-1] == "H":
        line["HEURE DEBUT"] = line["HEURE DEBUT"] + "00"
    if "h" not in line["HEURE DEBUT"] and "H" in line["HEURE DEBUT"]:
        time_tab = line["HEURE DEBUT"].split("H")
    else:
        time_tab = line["HEURE DEBUT"].split("h")
    i = 0
    for t in time_tab:
        if len(t) == 1:
            t = "0" + t
            time_tab[i] = t
            i += 1
    if time_tab[1] == "":
        time_tab.append("00")
    time_str = time_tab[0] + ":" + time_tab[1]
    return time_str


def get_other_ids():
    data = {}
    dataset = TDatasets.query.filter_by(dataset_name="STOM").one()
    data["dataset"] = dataset.id_dataset
    module = TModules.query.filter_by(module_code="stom").one()
    data["module"] = module.id_module
    return data


def parse_and_create_visit(line, site):
    ids = get_other_ids()
    # get uuid from the submission and use it has visit UUID
    visit_uuid = uuid.uuid4()
    heure = parse_time(line)
    # DB.session.query(TMonitoringVisits).filter_by(uuid_base_visit=visit_uuid).exitst()
    visit_dict_to_post = {
        "uuid_base_visit": visit_uuid,
        "id_dataset": ids["dataset"],
        "id_module": ids["module"],
        "data": {
            "heure": heure,
            "habitat_input": False,
            "debutant": "Non",
            "elem_paysager": None,
            "paturage": "5 - Inconnu",
            "sol_nu": None,
            "herb": None,
            "roche": None,
            "arb_inf_30cm": None,
            "arb_sup_4m": None,
            "arb_1_4m": None,
            "arb_inf_1m": None,
        },
    }
    visit_dict_to_post["id_base_site"] = site.id_base_site
    visit_dict_to_post["visit_date_min"] = parse_date(line)
    visit_dict_to_post["visit_date_max"] = parse_date(line)

    for col in line.keys():
        if col in [
            "SECTEUR PARC OU ZONE GEOGRAPHIQUE",
            "NOM SITE",
            "N°SECTEUR COMPTAGE",
            "NPOINT",
            "OBSERVATEUR 1",
            "DEBUTANT ?",
            "OBSERVATEUR 2",
            "DATE",
            "HEURE DEBUT",
            "ESPECE",
            "NB05",
            "NB510",
            "NB100",
            "MAX10",
            "NB1015",
            "Liste espèces",
            "RQ",
            "ZONE",
            "ID ZONE",
            "SECTEUR",
            "X",
            "Y",
            "ALT",
            "RASTALT",
            "INFOS SUP PATURAGE",
            "ID SITE",
        ]:
            pass
        else:
            val = line[col]
            mapping_nuage = {"1": "0-33%", "2": "33-66%", "3": "66-100%"}
            mapping_pluie = {
                "1": "1-Absente",
                "2": "2-Intermittente",
                "3": "3-Continue",
            }
            mapping_vent = {"1": "1-Absent", "2": "2-Faible", "3": "3-Moyen à fort"}
            mapping_visi = {"1": "1-Bonne", "2": "2-Modérée", "3": "3-Faible"}
            if col in ["AGRI", "IR", "IIR1", "IIR2"]:
                if val == "" or val == "NA":
                    val = None
                visit_dict_to_post["data"][col] = val
            elif col == "COUV NUAGE":
                val = mapping_nuage[val]
                visit_dict_to_post["data"]["nuages"] = val
            elif col == "PLUIE":
                val = mapping_pluie[val]
                visit_dict_to_post["data"]["pluie"] = val
            elif col == "VENT":
                val = mapping_vent[val]
                visit_dict_to_post["data"]["vent"] = val
            elif col == "VISI":
                val = mapping_visi[val]
                visit_dict_to_post["data"]["visi"] = val
            elif col == "DENEIGEMT" or col == "DENEIGMT":
                visit_dict_to_post["data"]["deneigement"] = val
            # elif col == "AGRI":
            #     tab = [
            #         "1 = Aucune trace de paturage dans le milieu",
            #         "2 = Toutes les situations intermédiaires",
            #         "3 = Plus de 95% des plantes herbacées sont pâturées et rases (<10 cm)",
            #         "4 = Prairie de fauche",
            #     ]
            else:
                visit_dict_to_post["data"]["habitat_input"] = True
                if val == "NA" or val == None or val == "NON":
                    val = None
                else:
                    if val != "":
                        if val[-1] == "%":
                            val = val[:-1]
                        val = int(val)
                    else:
                        val = None
                    if col in ["% SOL NU", "% ROCH", "% HERB"]:
                        if col == "% SOL NU":
                            visit_dict_to_post["data"]["sol_nu"] = val
                        elif col == "% ROCH":
                            visit_dict_to_post["data"]["roche"] = val
                        elif col == "% HERB":
                            visit_dict_to_post["data"]["herb"] = val
                    elif col in [
                        "ELEMENT PAYSAGE 1",
                        "ELEMENT PAYSAGE 2",
                        "ELEMENT PAYSAGE 3",
                    ]:
                        visit_dict_to_post["data"]["elem_paysager"] = []
                        for key in [
                            "ELEMENT PAYSAGE 1",
                            "ELEMENT PAYSAGE 2",
                            "ELEMENT PAYSAGE 3",
                        ]:
                            if line[key] != "":
                                tab = [
                                    {"value": "Câblage", "key": "Câblage"},
                                    {"value": "Point d'eau", "key": "Point d'eau"},
                                    {"value": "Clôture", "key": "Clôture"},
                                    {
                                        "value": "Groupe isolé d'arbres",
                                        "key": "Groupe isolé d'arbres",
                                    },
                                    {"value": "Ecobuage", "key": "Ecobuage"},
                                    {"value": "Bâti", "key": "Bâti"},
                                    {"value": "Falaise", "key": "Falaise"},
                                    {"value": "Autres", "key": "Autres"},
                                ]
                                visit_dict_to_post["data"]["elem_paysager"].append(
                                    str(
                                        line[key]
                                        + "-"
                                        + tab[(int(line[key]) - 1)]["value"]
                                    )
                                )
                        if visit_dict_to_post["data"]["elem_paysager"] == []:
                            visit_dict_to_post["data"]["elem_paysager"] = None
                    else:
                        if col == "%ARBRISSEAU" and "ARBRISSEAU_1m" in line.keys():
                            visit_dict_to_post["data"]["arb_inf_30cm"] = val
                        elif col == "%ARBRISSEAU_1m" or (
                            col == "%ARBRISSEAU" and "%ARBRISSEAU_1m" not in line.keys()
                        ):
                            visit_dict_to_post["data"]["arb_inf_1m"] = val
                        elif col == "%ARBUSTE":
                            visit_dict_to_post["data"]["arb_1_4m"] = val
                        elif col == "%ARBRES":
                            visit_dict_to_post["data"]["arb_sup_4m"] = val
    observers = parse_observers(line)
    visit = TMonitoringVisits(**visit_dict_to_post)
    visit.observers = observers
    return visit


def parse_and_create_observation(visit, cd_nom, line):
    observation_dict_to_post = {
        "uuid_observation": uuid.uuid4(),
        "data": {},
    }
    for col in ["NB05", "NB510", "NB1015", "MAX10", "NB100"]:
        try:
            val = line[col]
        except:
            val = 0
        if val == "":
            val = "0"
        if col == "MAX10" or col == "MAX 10":
            if val == "0":
                observation_dict_to_post["data"]["presence_juvenile"] = None
            else:
                observation_dict_to_post["data"]["presence_juvenile"] = int(val)
        else:
            if val == "NA":
                val = None
            if val is not None:
                val = int(val)
        if col == "NB05":
            observation_dict_to_post["data"]["nb_0_5"] = val
        elif col == "NB510":
            observation_dict_to_post["data"]["nb_5_10"] = val
        elif col == "NB1015":
            if val == "0" or val == 0:
                val = None
            observation_dict_to_post["data"]["nb_10_15"] = val
        elif col == "NB100":
            if val == "0" or val == 0:
                val = None
            observation_dict_to_post["data"]["nb_hors_proto"] = val
    observation_dict_to_post["cd_nom"] = cd_nom
    if "RQ" in line.keys():
        observation_dict_to_post["comments"] = line["RQ"]
    obs = TMonitoringObservations(**observation_dict_to_post)
    obs.id_base_visit = visit.id_base_visit
    return obs


def get_ods_file_data(file):
    data = json.dumps(get_data(file))
    return data


@click.command()
@click.option("--file-path", required=True)
@click.option("--error-file-path", default="error_output.csv")
def import_data(file_path, error_file_path):
    app = create_app()
    with app.app_context():
        data = get_data(file_path)
        added_obs = 0
        added_vis = 0
        n = 2
        errors = {
            "Site inconnu": [],
            "Observateur inconnu": [],
            "Observation déjà existante": [],
            "Taxon inconnu": [],
        }
        for line in data:
            skip_visite = False
            skip_obs = False
            print("line ", n)
            site = parse_site(line)
            date = parse_date(line)
            observers = parse_observers(line)
            if site is None:
                skip_visite = True
                errors["Site inconnu"].append((n, line))
            for ob in observers:
                if ob is None:
                    skip_visite = True
                    errors["Observateur inconnu"].append((n, line))
            if not skip_visite:
                visit = (
                    TMonitoringVisits.query.filter_by(visit_date_min=date)
                    .filter_by(id_base_site=site.id_base_site)
                    .one_or_none()
                )
                if visit is not None:
                    for obs in observers:
                        if obs not in visit.observers:
                            visit.observers.append(obs)
                if visit is None:
                    visit = parse_and_create_visit(line, site)
                    added_vis += 1
                    db.session.add(visit)
                tax = parse_taxon(line)
                if tax == -1:
                    skip_obs = True
                if not skip_obs:
                    obs = (
                        TMonitoringObservations.query.filter_by(
                            id_base_visit=visit.id_base_visit
                        )
                        .filter_by(cd_nom=tax)
                        .one_or_none()
                    )
                    if obs is not None:
                        errors["Observation déjà existante"].append((n, line))
                    elif tax is None:
                        errors["Taxon inconnu"].append((n, line))
                    else:
                        obs = parse_and_create_observation(visit, tax, line)
                        added_obs += 1
                        db.session.add(obs)
            n += 1
        keys = data[0].keys()
        write_errors_file(error_file_path, errors, keys)
        print(added_vis, " visites ajoutées\n", added_obs, " observations ajoutées")
        db.session.commit()


def write_errors_file(file_name, error_dict, keys):
    fields = ["LIGNE", "ERREUR"]
    for k in keys:
        fields.append(k)
    with open(file_name, "a") as file:
        dw = csv.DictWriter(file, fieldnames=fields)
        for key in error_dict.keys():
            if error_dict[key] != []:
                tw = {}
                for e in error_dict[key]:
                    tw["LIGNE"] = e[0]
                    tw["ERREUR"] = key
                    for k in keys:
                        tw[k] = e[1][k]
                    dw.writerow(tw)


def parse_visit_data(file_name):
    data = get_data(file_name)
    for line in data:
        site = parse_site(line)
        date = parse_date(line)
        if site is None:
            print(
                "ATTENTION: Site ",
                line["NOM SITE"] + "-" + line["NPOINT"],
                "non trouvé dans la BDD.",
            )
        else:
            visit = (
                TMonitoringVisits.query.filter_by(visit_date_min=date)
                .filter_by(id_base_site=site.id_base_site)
                .one_or_none()
            )
            if visit is None:
                print(
                    "ATTENTION: Pas de visite trouvée pour le site ",
                    site.base_site_name,
                    " à la date ",
                    date,
                )
            else:
                data = visit.data
                if line["COMMENTAIRES"] is not None:
                    visit.comments = line["COMMENTAIRES"]
                for col in [
                    "HABITAT PRINCIPAL",
                    "HABITAT SECONDAIRE1",
                    "HABITAT SECONDAIRE2",
                    "ACTIVITE AGRICOLE",
                    "SOL NU/ROCHERS  sp dom",
                    "HERBACEE  sp dom",
                    "ARBRISSEAU   sp dom",
                    "ARBUSTE   sp dom",
                    "ARBRES   sp dom",
                ]:
                    val = line[col]
                    if val == "":
                        val = None
                    data[col] = val
                for elt in [
                    "paturage",
                    "herb",
                    "roche",
                    "sol_nu",
                    "arb_inf_30cm",
                    "arb_inf_1m",
                    "arb_1_4m",
                    "arb_sup_4m",
                    "elem_paysager",
                ]:
                    if data[elt] is None:
                        if elt == "elem_paysager":
                            data["elem_paysager"] = []
                            tab = [
                                {"value": "Câblage", "key": "Câblage"},
                                {"value": "Point d'eau", "key": "Point d'eau"},
                                {"value": "Clôture", "key": "Clôture"},
                                {
                                    "value": "Groupe isolé d'arbres",
                                    "key": "Groupe isolé d'arbres",
                                },
                                {"value": "Ecobuage", "key": "Ecobuage"},
                                {"value": "Bâti", "key": "Bâti"},
                                {"value": "Falaise", "key": "Falaise"},
                                {"value": "Autres", "key": "Autres"},
                            ]
                            for pays in [
                                "ELEMENT PAYSAGE 1",
                                "ELEMENT PAYSAGE 2",
                                "ELEMENT PAYSAGE 3",
                            ]:
                                if line[pays] == "":
                                    line[pays] = None
                                if line[pays] is not None:
                                    data["elem_paysager"].append(
                                        tab[int(line[pays][0])]
                                    )
                                    if len(line[pays]) > 1:
                                        data["comment_paysage"] = line[pays][
                                            2 : len(line[pays]) - 1
                                        ]
                            if data["elem_paysager"] == []:
                                data["elem_paysager"] = None
                        if elt == "sol_nu":
                            if line["SOL NU/ROCHERS  % rec"] == "":
                                data["elt"] = None
                            else:
                                data[elt] = int(line["SOL NU/ROCHERS  % rec"])
                        if elt == "herb":
                            if line["HERBACEE % rec"] == "":
                                data["elt"] = None
                            else:
                                data[elt] = line["HERBACEE % rec"]
                        if elt == "arb_inf_1m":
                            if line["ARBRISSEAU  % rec"] == "":
                                data[elt] = None
                            else:
                                data[elt] = int(line["ARBRISSEAU  % rec"])
                        if elt == "arb_1_4m":
                            if line["ARBRISSEAU  % rec"] == "":
                                data[elt] = None
                            else:
                                data[elt] = int(line["ARBRISSEAU  % rec"])
                        if elt == "arb_sup_4m":
                            if line["ARBRES % rec"] == "":
                                data[elt] = None
                            else:
                                data[elt] = int(line["ARBRES % rec"])
                TMonitoringVisits.session.query(
                    id_base_visit=visit.id_base_visit
                ).update(data=data)
                print(
                    "Visite ",
                    visit.id_base_visit,
                    " @ site ",
                    site.base_site_name,
                    " mis à jour",
                )
        db.session.commit()


if __name__ == "__main__":
    import_data()
