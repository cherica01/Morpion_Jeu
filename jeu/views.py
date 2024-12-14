from django.shortcuts import render
from django.http import JsonResponse
import json

# Plateau initial vide
PLATEAU_VIDE = [["", "", ""], ["", "", ""], ["", "", ""]]

# Vérifie si un joueur a gagné
def verifier_victoire(plateau, joueur):
    # Vérification des lignes
    for ligne in plateau:
        if all(case == joueur for case in ligne):
            return True
    # Vérification des colonnes
    for col in range(3):
        if all(plateau[ligne][col] == joueur for ligne in range(3)):
            return True
    # Vérification des diagonales
    if all(plateau[i][i] == joueur for i in range(3)) or all(plateau[i][2 - i] == joueur for i in range(3)):
        return True
    return False

# Vérifie si le plateau est plein
def est_plein(plateau):
    return all(case != "" for ligne in plateau for case in ligne)

# Algorithme Minimax pour l'IA
def minimax(plateau, profondeur, maximiser):
    joueur_humain = "X"
    joueur_ordinateur = "O"

    # Conditions de fin de partie
    if verifier_victoire(plateau, joueur_ordinateur):
        return 10 - profondeur
    if verifier_victoire(plateau, joueur_humain):
        return profondeur - 10
    if est_plein(plateau):
        return 0

    # Maximisation (IA)
    if maximiser:
        meilleur_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if plateau[i][j] == "":
                    plateau[i][j] = joueur_ordinateur
                    score = minimax(plateau, profondeur + 1, False)
                    plateau[i][j] = ""
                    meilleur_score = max(meilleur_score, score)
        return meilleur_score
    # Minimisation (Humain)
    else:
        meilleur_score = float('inf')
        for i in range(3):
            for j in range(3):
                if plateau[i][j] == "":
                    plateau[i][j] = joueur_humain
                    score = minimax(plateau, profondeur + 1, True)
                    plateau[i][j] = ""
                    meilleur_score = min(meilleur_score, score)
        return meilleur_score

# Détermine le meilleur coup pour l'IA
def meilleur_coup(plateau):
    meilleur_score = -float('inf')
    coup = None
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == "":
                plateau[i][j] = "O"
                score = minimax(plateau, 0, False)
                plateau[i][j] = ""
                if score > meilleur_score:
                    meilleur_score = score
                    coup = (i, j)
    return coup

# Vue principale du jeu
def jeu_morpion(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            plateau = data.get("plateau", [])
            ligne = data.get("ligne", -1)
            colonne = data.get("colonne", -1)

            # Validation des données
            if not (0 <= ligne < 3 and 0 <= colonne < 3):
                return JsonResponse({"error": "Coup invalide"}, status=400)
            if plateau[ligne][colonne] != "":
                return JsonResponse({"error": "Case déjà occupée"}, status=400)

            # Le joueur humain joue son coup
            plateau[ligne][colonne] = "X"

            # Vérifie la victoire ou si le plateau est plein
            if verifier_victoire(plateau, "X"):
                return JsonResponse({"plateau": plateau, "victoire": "X", "plein": False})
            if est_plein(plateau):
                return JsonResponse({"plateau": plateau, "victoire": None, "plein": True})

            # L'IA joue son tour
            coup = meilleur_coup(plateau)
            if coup:
                plateau[coup[0]][coup[1]] = "O"

            # Vérifie la victoire après le coup de l'IA
            victoire_ia = verifier_victoire(plateau, "O")
            plein = est_plein(plateau)

            return JsonResponse({
                "plateau": plateau,
                "victoire": "O" if victoire_ia else None,
                "plein": plein
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Données invalides"}, status=400)

    # GET : Charge l'interface du jeu
    return render(request, "jeu/morpion.html", {"plateau": PLATEAU_VIDE})
