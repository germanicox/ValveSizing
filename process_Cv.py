from flask import Flask, render_template, request, jsonify, url_for

from fluids import *
from scipy.constants import *
from fluids.control_valve import size_control_valve_l
from thermo.chemical import Chemical

def F_to_m3_seg(data) :
    if data['flow_unit'] == "gpm" :
        return float(data['flow_Min'])*0.00006309
    if data['flow_unit'] == "ton_hr" :
        return float(data['flow_Min'])*0.00028
    if data['flow_unit'] == "m3_hr" :
        return float(data['flow_Min'])*0.00028
    if data['flow_unit'] == "m3_seg" :
        return float(data['flow_Min'])

def P_to_Pascal(data) : 
    if data['press_unit'] == "psi" :
        return float(data['P1_Min'])* 6894.75728 , float(data['P2_Min'])* 6894.75728
    if data['press_unit'] == "bar" :
        return float(data['P1_Min'])* 100000 , float(data['P2_Min'])* 100000
    if data['press_unit'] == "kPascal" :
        return float(data['P1_Min']) , float(data['P2_Min'])
    if data['press_unit'] == "kPascal" :
        return float(data['P1_Min'])*1000 , float(data['P2_Min'])*1000

def T_to_K(data) :
    if data['temp_unit'] == "C":
        return float(data['temp_Min'])+273.15
    if data['temp_unit'] == "F":
        return (float(data['temp_Min']) - 32)*5/9 + 273.15
    if data['temp_unit'] == "K":
        return float(data['temp_Min']) 

def D_to_meter(data) :
    if data['pipe_unit'] == "in" :
        return float(data['inletD'])*0.0254 , float(data['outletD'])*0.0254
    if data['pipe_unit'] == "mm" :
        return float(data['inletD'])*0.001 , float(data['outletD'])*0.001
    if data['pipe_unit'] == "m" :
        return float(data['inletD']) , float(data['outletD'])


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('flowComputing.html')


@app.route('/process', methods=['POST'])
def process():

# loading variables from JSON
    json_data = request.form

# Diameter in meters (Pipe ID) Pressure in Pascal , Flow in m3-seg and T in Kelvin for Cv computation
    
    P1 , P2 =  P_to_Pascal(json_data)
    F = F_to_m3_seg(json_data)
    T = T_to_K(json_data)
    D1 , D2 = D_to_meter(json_data)
    d = 0.0381


    valida_data = True

    if valida_data:
        liquid = Chemical(json_data['liquid'], P=(P1+P2)/2, T=T)
        rho = liquid.rho
        Psat = liquid.Psat
        Pc = liquid.Pc
        mu = liquid.mu

        sizing = size_control_valve_l(rho, Psat, Pc, mu, P1, P2, F, D1, D2, d, FL=0.99, Fd=1, full_output=True)
        Cav_index = round(cavitation_index(P1=P1, P2=P2, Psat=Psat), 4)
        Cv = round(Kv_to_Cv(sizing['Kv']), 4)
        print('Cv: ', Cv )
        print('Cavitation index: ', Cav_index)
        return jsonify({'Cv':Cv, 'Cav_index':Cav_index })

    return jsonify({'error':'Missing data!'})



if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host = '0.0.0.0', port=5000)