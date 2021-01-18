import React, { Component, useEffect, useState } from 'react';
import {Tabs, Tab   } from '@material-ui/core';
import Chart from "./Measurements/Chart";
import LoadMeasurements from "./Measurements/LoadMeasurements";
import FurfuralMeasurements from "./Measurements/FurfuralMeasurements"
import OilQualityMeasurements from "./Measurements/OilQualityMeasurements"
import DissolvedGasesMeasurements from "./Measurements/DissolvedGasesMeasurements"

/*export default class TransformerPage extends Component {
    constructor(props) {
        super(props);
        this.transformerId = this.props.match.params.transformerId;
        this.state = {
            measurements: null
        }
    }

    componentDidMount() {
        this.transformerMeasurementsGet();
    }

    transformerMeasurementsGet() {
        fetch('/api/transformers/'+ this.transformerId + '/medicoes', {
            method: "GET"
        })
          .then( (response) => {
                console.log(response);
                console.log("estamos aqui cabrao");
                return response.json();
          })
          .then( (obj) => {
                console.log(obj);
                this.setState({
                    measurements: {
                        load: obj.load,
                        dissolved_gases: obj.dissolved_gases,
                        furfural: obj.furfural,
                        oil_quality: obj.oil_quality,
                    }
                })
          });
    }

    render() {
        if (this.state.measurements) {
            console.log("this is transformerPage render");
            return (
                <div>
                    <h3>Load Measurements</h3>
                    <LoadMeasurements loadData={this.state.measurements.load}/>
                    <h3>Furfural Measurements</h3>
                    <FurfuralMeasurements furfuralData={this.state.measurements.furfural}/>
                    <h3>Oil Quality Measurements</h3>
                    <OilQualityMeasurements oilQualityData={this.state.measurements.oil_quality}/>
                    <h3>Dissolved Gases Measurements</h3>
                    <DissolvedGasesMeasurements measurements={this.state.measurements.dissolved_gases}/>
                </div>
            );
        }
        return <h1>TransformerPage</h1>;
    }
}*/

export default function TransformerPage(props) {

    const [measurementsData, setMeasurementsData] = useState({})
    useEffect(() => {
        const url = "http://localhost:8000/api/transformers/"
        fetch(url + props.match.params.transformerId + "/medicoes", {
            method: "GET" 
        })
        .then((response) => response.json())
        .then((obj) => {
            setMeasurementsData({
                load: obj.load,
                furfural: obj.furfural,
                dissolved_gases: obj.dissolved_gases,
                oil_quality: obj.oil_quality
            })
        })
        .catch(() => {
            console.log("Can't access: " + url);
        })
        
    }, [setMeasurementsData])
    
    console.log(measurementsData)
    return (
        <div>
            <h1 className="main-title">Transformer {props.match.params.transformerId}</h1>
            <LoadMeasurements 
              data={measurementsData.load}
            />
        </div>
    );
}