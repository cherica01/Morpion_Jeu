from django.shortcuts import render
from django.http import JsonResponse
import json

PLATEAU_VIDE = [["", "", ""], ["", "", ""], ["", "", ""]]

def verifier_victoire(plateau, joueur):
    for ligne in plateau:
        if all(case == joueur for case in ligne):
            return True
    for col in range(3):
        if all(plateau[ligne][col] == joueur for ligne in range(3)):
            return True
    if all(plateau[i][i] == joueur for i in range(3)) or all(plateau[i][2 - i] == joueur for i in range(3)):
        return True
    return False

def est_plein(plateau):
    return all(case != "" for ligne in plateau for case in ligne)

def minimax(plateau, profondeur, maximiser):
    joueur_humain = "X"
    joueur_ordinateur = "O"

    if verifier_victoire(plateau, joueur_ordinateur):
        return 10 - profondeur
    if verifier_victoire(plateau, joueur_humain):
        return profondeur - 10
    if est_plein(plateau):
        return 0

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

def jeu_morpion(request):
    if request.method == "POST":
        try:
            plateau = json.loads(request.POST.get("plateau", "[]"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid data format"}, status=400)

        coup = meilleur_coup(plateau)
        if coup:
            plateau[coup[0]][coup[1]] = "O"
        victoire = verifier_victoire(plateau, "O")
        plein = est_plein(plateau)

        return JsonResponse({
            "plateau": plateau,
            "victoire": victoire,
            "plein": plein
        })

    return render(request, "jeu/morpion.html", {"plateau": PLATEAU_VIDE})