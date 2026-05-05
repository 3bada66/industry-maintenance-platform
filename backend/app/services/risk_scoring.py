# backend/app/services/risk_scoring.py
from datetime import datetime
from typing import Dict, Any, List


class CompositeRiskScoringEngine:
    """
    Calcolo risk score composito per asset industriali:
    - Vulnerabilità (35%)
    - Impatto (40%)
    - Operativo (25%)
    Breakdown dettagliato, gestione dati mancanti, suggerimenti punti deboli.
    """

    VULN_WEIGHT = 0.35
    IMPACT_WEIGHT = 0.40
    OPER_WEIGHT = 0.25

    TRANSLATIONS = {
        "en": {
            "remote_access_enabled": "Remote access enabled (+2)",
            "remote_access_unattended": "Unattended remote access (+2)",
            "physical_access_easy": "Easy physical access (+3)",
            "physical_access_medium": "Medium physical access (+1)",
            "purdue_low_high_connection": "Low Purdue level connected to high levels (+3)",
            "connections_count": "{n} connections (+{add})",
            "business_criticality": "Business criticality: {crit} ({score})",
            "purdue_low": "Low Purdue (+2)",
            "missing_business_criticality": "Missing business criticality: cannot calculate risk.",
            "suggest_disable_remote": "Disable remote access if not needed.",
            "suggest_avoid_unattended": "Avoid unattended remote access.",
            "suggest_harden_physical": "Make physical access harder.",
            "suggest_isolate_purdue": "Isolate low Purdue level assets from high levels.",
            "suggest_reduce_connections": "Reduce unnecessary connections.",
            "suggest_set_criticality": "Set business criticality for accurate calculation.",
        },
        "it": {
            "remote_access_enabled": "Accesso remoto abilitato (+2)",
            "remote_access_unattended": "Accesso remoto unattended (+2)",
            "physical_access_easy": "Accesso fisico facile (+3)",
            "physical_access_medium": "Accesso fisico medio (+1)",
            "purdue_low_high_connection": "Livello Purdue basso connesso a livelli alti (+3)",
            "connections_count": "{n} connessioni (+{add})",
            "business_criticality": "Criticità business: {crit} ({score})",
            "purdue_low": "Purdue basso (+2)",
            "missing_business_criticality": "Criticità business mancante: impossibile calcolare il rischio.",
            "suggest_disable_remote": "Disabilita l’accesso remoto se non necessario.",
            "suggest_avoid_unattended": "Evita accesso remoto unattended.",
            "suggest_harden_physical": "Rendi più difficile l’accesso fisico.",
            "suggest_isolate_purdue": "Isola asset di livello Purdue basso da livelli alti.",
            "suggest_reduce_connections": "Riduci il numero di connessioni non necessarie.",
            "suggest_set_criticality": "Imposta la criticità business per un calcolo accurato.",
        },
    }

    CRIT_MAP = {"low": 2, "medium": 5, "high": 8, "critical": 10}
    CRIT_TRANSLATIONS = {
        "en": {
            "low": "low",
            "medium": "medium",
            "high": "high",
            "critical": "critical",
        },
        "it": {
            "low": "bassa",
            "medium": "media",
            "high": "alta",
            "critical": "critica",
        },
    }

    def calculate(self, asset, language="en") -> Dict[str, Any]:
        translations = self.TRANSLATIONS.get(language, self.TRANSLATIONS["en"])
        crit_trans = self.CRIT_TRANSLATIONS.get(language, self.CRIT_TRANSLATIONS["en"])
        missing = []
        suggestions = []
        # --- Vulnerabilities ---
        vuln_score = 1
        vuln_break = []
        # Accesso remoto
        if getattr(asset, "remote_access", None):
            vuln_score += 2
            vuln_break.append(translations["remote_access_enabled"])
            if getattr(asset, "remote_access_type", None) == "unattended":
                vuln_score += 2
                vuln_break.append(translations["remote_access_unattended"])
        # Physical access ease
        phys = getattr(asset, "physical_access_ease", None)
        if phys == "easy":
            vuln_score += 3
            vuln_break.append(translations["physical_access_easy"])
        elif phys == "medium":
            vuln_score += 1
            vuln_break.append(translations["physical_access_medium"])
        elif phys is None:
            missing.append("physical_access_ease")
        # Purdue "inappropriato"
        purdue = getattr(asset, "purdue_level", None)
        if purdue is not None:
            if purdue in [0, 1] and self._has_direct_high_level_connection(asset):
                vuln_score += 3
                vuln_break.append(translations["purdue_low_high_connection"])
        else:
            missing.append("purdue_level")
        # Numero connessioni
        n_conn = len(getattr(asset, "connections", []) or [])
        if n_conn:
            add_conn = n_conn // 5
            vuln_score += add_conn
            if add_conn:
                vuln_break.append(
                    translations["connections_count"].format(n=n_conn, add=add_conn)
                )
        # TODO: connessioni a asset critici
        # --- Impatto ---
        imp_score = None
        imp_break = []
        crit = getattr(asset, "business_criticality", None)
        crit_map = self.CRIT_MAP
        crit_key = None
        if crit:
            crit_lower = str(crit).lower()
            for k in crit_map:
                if crit_lower == k or crit_lower == self.CRIT_TRANSLATIONS["it"].get(k):
                    crit_key = k
                    break
        if crit_key in crit_map:
            imp_score = crit_map[crit_key]
            imp_break.append(
                translations["business_criticality"].format(
                    crit=crit_trans[crit_key], score=imp_score
                )
            )
        else:
            missing.append("business_criticality")
        # Modifica per Purdue
        if purdue is not None and imp_score is not None:
            if purdue in [0, 1, 2]:
                imp_score += 2
                imp_break.append(translations["purdue_low"])
        # Dipendenze critiche (placeholder: nessuna logica, da implementare)
        # --- Operativo ---
        oper_score = imp_score
        oper_break = [*imp_break]
        # (puoi differenziare la logica operativa in futuro)
        # --- Normalizzazione ---
        vuln_score = min(10, max(1, vuln_score))
        if imp_score is not None:
            imp_score = min(10, max(1, imp_score))
        if oper_score is not None:
            oper_score = min(10, max(1, oper_score))
        # --- Calcolo finale ---
        if imp_score is None or oper_score is None:
            final_score = None
            suggestions.append(translations["missing_business_criticality"])
        else:
            final_score = round(
                self.VULN_WEIGHT * vuln_score
                + self.IMPACT_WEIGHT * imp_score
                + self.OPER_WEIGHT * oper_score,
                2,
            )
        # --- Suggerimenti punti deboli ---
        if getattr(asset, "remote_access", None):
            suggestions.append(translations["suggest_disable_remote"])
        if getattr(asset, "remote_access_type", None) == "unattended":
            suggestions.append(translations["suggest_avoid_unattended"])
        if phys == "easy":
            suggestions.append(translations["suggest_harden_physical"])
        if purdue in [0, 1] and self._has_direct_high_level_connection(asset):
            suggestions.append(translations["suggest_isolate_purdue"])
        if n_conn > 10:
            suggestions.append(translations["suggest_reduce_connections"])
        if "business_criticality" in missing:
            suggestions.append(translations["suggest_set_criticality"])
        # --- Breakdown ---
        breakdown = {
            "vulnerability": {"score": vuln_score, "breakdown": vuln_break},
            "impact": {"score": imp_score, "breakdown": imp_break},
            "operational": {"score": oper_score, "breakdown": oper_break},
            "weights": {
                "vulnerability": self.VULN_WEIGHT,
                "impact": self.IMPACT_WEIGHT,
                "operational": self.OPER_WEIGHT,
            },
            "final_score": final_score,
            "missing_data": missing,
            "suggestions": suggestions,
        }
        return breakdown

    def _has_direct_high_level_connection(self, asset) -> bool:
        # Placeholder: implementa logica reale se hai info sulle connessioni
        # Es: controlla se asset.connections contiene asset con purdue_level >= 4
        return False
