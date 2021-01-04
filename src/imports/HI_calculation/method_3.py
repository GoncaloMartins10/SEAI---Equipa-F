import numpy as np
import math
import json
import os

from .fetch_data import *
from ..resources.db_classes import *

class MultiFeatureIndex():

    # def __init__(self,
    #              pesos_combinado = def_combinado, 
    #              pesos_main = def_main,
    #              pesos_iso= def_iso, 
    #              pesos_CH = def_CH, 
    #              pesos_oil = def_oil):
    #     # definir constantes
    #     self.pesos_main = pesos_main
    #     self.pesos_iso= pesos_iso
    #     self.pesos_CH = pesos_CH
    #     self.pesos_oil = pesos_oil
    #     self.pesos_combinado = pesos_combinado

    #     self.caluculate_indexes()

    def read_json():
        cwd = os.getcwd()
        repo_name = 'SEAI---Equipa-F'
        repo_dir = cwd[:cwd.rindex(repo_name) + len(repo_name)] # retira tudo depois de 'SEAI---Equipa-F'
        weight_path = os.path.join(repo_dir,"src/imports/HI_calculation/weights.json")

        with open(weight_path, "r") as file: 
            config = json.load(file)
            return config["method_3"]

    def __init__(self):
        read_json = read_json()
        
        self.pesos_main = read_jason["pesos_main"]
        self.pesos_iso= read_jason["pesos_iso"]
        self.pesos_CH = read_json["pesos_CH"]
        self.pesos_oil = read_json["pesos_oil"]
        self.pesos_combinado = read_json["pesos_combinado"]

        #self.caluculate_indexes()


    def read_pesos():
        
        print(pesos_main['HI0'])

    # def caluculate_indexes(self):
    #     self.main = self.get_main()
    #     self.iso = self.get_iso()
    #     self.CH = self.get_CH()
    #     self.oil = self.get_oil()
    #     self.combinado = self.get_combinado()

    # def combinado(self):
    #     w=np.array(list(self.pesos_combinado.values()))

    #     HI=np.array([            # Funções dos índices
    #         self.main, 
    #         self.iso, 
    #         self.CH, 
    #         self.oil,
    #     ])
    #     # Calcular somatório
    #     HI_com = np.sum(w * HI)
    #     print("Indice de vida:", HI_com)
        


    # def get_main(pesos):
    #     pesos = self.pesos_main
    #     B = pesos['f_L'] * (np.log(6.5/0.5) / pesos['t_exp'])     # Coeficiente de envelhecimento
    #     HI_m = pesos['HI0'] * math.exp(B * (pesos['T2'] - pesos['T1']))
    #     return HI_m

    # def get_iso(): 
    #     w_F_CO = self.pesos_iso['w_F_CO']
    #     x = self.pesos_iso["x"]
    #     # Inicializar Fator Oxigénio-Carbono
    #     a = np.matrix([[0.0067, 0.008 , 0.0006  ]
    #                    [0.0017, 0.0033, 0.00014 ],
    #                    [0.02  , 0.0005, 0.000033],
    #                    [0.0125, 0.0008, 9.44e-6 ],
    #                    [0     , 0.0003, 0       ]])
        
    #     b = np.matrix([[0     , 0   , 0   ],
    #                    [1.5   , -6.0, 1.59],
    #                    [-14.97, 2.4 , 2.66],
    #                    [-7.5  , 0.9 , 6.65],
    #                    [0     , 5.9 , 0   ]])

    #     cond = np.matrix([[x["CO"] in range(0,300)     , x["CO2"] in range(0,2400)      , x["CO_CO2"] in range(0,3000)        ],
    #                       [x["CO"] in range(300,900)   , x["CO2"] in range(2400, 3000)  , x["CO_CO2"] in range(3000,10000)    ],
    #                       [x["CO"] in range(900, 1000) , x["CO2"] in range(3000, 5000)  , x["CO_CO2"] in range(10000, 170000) ],
    #                       [x["CO"] in range(1000, 1400), x["CO2"] in range(5000, 10000) , x["CO_CO2"] in range(170000, 350000)],
    #                       [x["CO"] > 1400              , x["CO2"] in range(10000, 13000), x["CO_CO2"] > 350000                ]])
    #     F_CO = dict();

    #     dot_product = lambda x,y: int(np.dot(np.transpose(x), y))

    #     a_k, b_k = dot_product(a[:,0], cond[:,0]) , dot_product(b[:,0], cond[:,0])
    #     F_CO["CO"] = a_k * x["CO"] + b_k if (a_k, b_k) != (0, 0) else 10

    #     a_k, b_k = dot_product(a[:,1], cond[:,1]) , dot_product(b[:,1], cond[:,1])
    #     F_CO["CO2"] = a_k * x["CO2"] + b_k if (a_k, b_k) != (0, 0) else 10

    #     a_k, b_k = dot_product(a[:,2], cond[:,2]) , dot_product(b[:,2], cond[:,2])
    #     F_CO["CO_CO2"] = a_k * x["CO_CO2"] + b_k if (a_k, b_k) != (0, 0) else 10

    #     F_CO_vector = np.array(list(F_CO.values()))
    #     C_fur = 1
    #     # Calcular o indíce HI_C,O
    #     HI_CO = np.sum(w_F_CO * F_CO_vector)
    #     HI_fur = 3.344 * C_fur**0.413   # Calcular HI_fur

    #     w1 = 0.3
    #     w2 = 0.7
    #     HI_iso = w1 * HI_CO + w2 * HI_fur
    #     return HI_iso

    # def get_CH():
    #     w_CH = np.array([
    #         0.2310,         # H2
    #         0.2306,         # CH4
    #         0.0772,         # C2H6
    #         0.2301,         # C2H4
    #         0.2312          # C2H2
    #     ])

    #     F_CH = np.array([   # Inicializar vetor
    #         0,
    #         0,
    #         0,
    #         0,
    #         0
    #     ])

    #     # Fatores Xi (uL/L) | VALORES ALTERÁVEIS
    #     x_CH = np.array([
    #         50,             # H2
    #         15,             # CH4
    #         20,             # C2H6
    #         10,             # C2H4
    #         3               # C2H2
    #     ])

    #     # Calcular F_C,H dos diferentes gases consoante o seu conteúdo (uL/L)
    #     # H2
    #     if x_CH[0] <= 30:               
    #         F_CH[0] = 0
    #     elif 30 < x_CH[0] <= 50:
    #         F_CH[0] = 0.1*x_CH[0] - 3 
    #     elif 50 < x_CH[0] <= 100:
    #         F_CH[0] = 0.06*x_CH[0] + 1
    #     elif 100 < x_CH[0] <= 500:
    #         F_CH[0] = 0.0125*x_CH[0] + 3.75
    #     else:
    #         F_CH[0] = 10
        
    #     # CH4
    #     if x_CH[1] <= 10:               
    #         F_CH[1] = 0
    #     elif 10 < x_CH[1] <= 15:
    #         F_CH[1] = 0.4*x_CH[1] - 2 
    #     elif 15 < x_CH[1] <= 115:
    #         F_CH[1] = 0.0727*x_CH[1] + 0.9
    #     else:
    #         F_CH[1] = 10

    #     # C2H6
    #     if x_CH[2] <= 5:               
    #         F_CH[2] = 0
    #     elif 5 < x_CH[2] <= 20:
    #         F_CH[2] = 0.1333*x_CH[2] - 0.6667 
    #     elif 20 < x_CH[2] <= 35:
    #         F_CH[2] = 0.2*x_CH[2] - 2
    #     elif 35 < x_CH[2] <= 70:
    #         F_CH[2] = 0.125*x_CH[2] + 0.625
    #     else:
    #         F_CH[2] = 10
        
    #     # C2H4
    #     if x_CH[3] <= 10:               
    #         F_CH[3] = 0
    #     elif 10 < x_CH[3] <= 30:
    #         F_CH[3] = 0.1*x_CH[3] - 1
    #     elif 30 < x_CH[3] <= 50:
    #         F_CH[3] = 0.15*x_CH[3] - 2.5
    #     elif 50 < x_CH[3] <= 175:
    #         F_CH[3] = 0.04*x_CH[3] + 3
    #     else:
    #         F_CH[3] = 10

    #     # C2H2
    #     if x_CH[4] <= 0.5:               
    #         F_CH[4] = 0
    #     elif 0.5 < x_CH[4] <= 3:
    #         F_CH[4] = 0.8*x_CH[4] - 0.4
    #     elif 3 < x_CH[4] <= 5:
    #         F_CH[4] = 1.5*x_CH[4] - 2.5
    #     elif 5 < x_CH[4] <= 35:
    #         F_CH[4] = 0.1667*x_CH[4] + 4.167
    #     else:
    #         F_CH[4] = 10

    #     HI_CH = w_CH * F_CH

    #     return np.sum(HI_CH)

    # def get_oil():
    #     w_oil = np.array([  # peso dos fatores
    #         0.4565,         # mw
    #         0.2598,         # av
    #         0.1386,         # dl
    #         0.1452          # bv
    #     ])

    #     F_oil = np.array([   # Inicializar vetor de fator de qualidade do óleo
    #         0,
    #         0,
    #         0,
    #         0
    #     ])

    #     # Fatores que influenciam a qualidade do óleo | VALORES ALTERÁVEIS
    #     mw = 30             # Micro-Water (mg/L)
    #     av = 0.2            # Acid Value (mgKOH/g)
    #     dl = 0.5            # Dielectric Loss (25ºC)
    #     bv = 43             # Breakdown Voltage (kV)

    #     # Calcular fatores de qualidade
    #     # Micro-Water
    #     if mw <= 20:
    #         F_oil[0] = 0
    #     elif 20 < mw <= 30:
    #         F_oil[0] = 0.2*mw - 4
    #     elif 30 < mw <= 45:
    #         F_oil[0] = 0.4*mw - 10
    #     else:
    #         F_oil[0] = 10

    #     # Acid Value
    #     if av <= 0.015:
    #         F_oil[1] = 0
    #     elif 0.015 < av <= 0.1:
    #         F_oil[1] = 23.53*av - 0.353
    #     elif 0.1 < av <= 0.2:
    #         F_oil[1] = 20*av 
    #     elif 0.2 < av <= 0.3:
    #         F_oil[1] = 40*av - 4
    #     else:
    #         F_oil[1] = 10

    #      # Dielectric Loss
    #     if dl <= 0.005:
    #         F_oil[2] = 0
    #     elif 0.005 < dl <= 0.015:
    #         F_oil[2] = 20*dl - 1
    #     elif 0.015 < dl <= 0.5:
    #         F_oil[2] = 5.714*dl + 1.143
    #     elif 0.5 < dl <= 1.5:
    #         F_oil[2] = 4*dl + 2
    #     else:
    #         F_oil[2] = 10
        
    #     # Breakdown Voltage
    #     if bv <= 30:
    #         F_oil[3] = 10
    #     elif 30 < bv <= 40:
    #         F_oil[3] = -0.4*bv + 20
    #     elif 40 < bv <= 43:
    #         F_oil[3] = -0.664*bv + 30.68
    #     elif 43 < bv <= 45:
    #         F_oil[3] = -1*bv + 45
    #     else:
    #         F_oil[3] = 0
        
    #     # Calcular índice
    #     HI_oil = w_oil * F_oil

    #     return np.sum(HI_oil)
