"""
    Tabela 5.2 pg.70
    Quantidade de calcário (PRNT 100%) necessário para elevar o Ph do solo
    da camada de 0 a 20cm, a 5.5, 6 e 6.5, estimadas pelo indice SMP.
 """

TABLE_5_2 = {
    4.4: {5.5: 15,      6: 21,      6.5: 29},
    4.5: {5.5: 12.5,    6: 17.3,    6.5: 24},
    4.6: {5.5: 10.9,    6: 15.1,    6.5: 20},
    4.7: {5.5: 9.6,     6: 13.3,    6.5: 17.5},
    4.8: {5.5: 8.5,     6: 11.9,    6.5: 15.7},
    4.9: {5.5: 7.7,     6: 10.7,    6.5: 14.2},

    5:   {5.5: 6.6,     6: 9.9,     6.5: 13.3},
    5.1: {5.5: 6,       6: 9.1,     6.5: 12.3},
    5.2: {5.5: 5.3,     6: 8.3,     6.5: 11.3},
    5.3: {5.5: 4.8,     6: 7.5,     6.5: 10.4},
    5.4: {5.5: 4.2,     6: 6.8,     6.5: 9.5},
    5.5: {5.5: 3.7,     6: 6.1,     6.5: 8.6},
    5.6: {5.5: 3.2,     6: 5.4,     6.5: 7.8},
    5.7: {5.5: 2.8,     6: 4.8,     6.5: 7},
    5.8: {5.5: 2.3,     6: 4.2,     6.5: 6.3},
    5.9: {5.5: 2,       6: 3.7,     6.5: 5.6},

    6:   {5.5: 1.6,     6: 3.2,     6.5: 4.9},
    6.1: {5.5: 1.3,     6: 2.7,     6.5: 4.3},
    6.2: {5.5: 1,       6: 2.2,     6.5: 3.7},
    6.3: {5.5: 0.8,     6: 1.8,     6.5: 3.1},
    6.4: {5.5: 0.6,     6: 1.4,     6.5: 2.6},
    6.5: {5.5: 0.4,     6: 1.1,     6.5: 2.1},
    6.6: {5.5: 0.2,     6: 0.8,     6.5: 1.6},
    6.7: {5.5: 0,       6: 0.5,     6.5: 1.2},
    6.8: {5.5: 0,       6: 0.3,     6.5: 0.8},
    6.9: {5.5: 0,       6: 0.2,     6.5: 0.5},

    7:   {5.5: 0,       6: 0,       6.5: 0.2},
    7.1: {5.5: 0,       6: 0,       6.5: 0},
}
