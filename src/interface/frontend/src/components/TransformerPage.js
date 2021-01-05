import React, { Component } from 'react';
import {Tabs, Tab   } from '@material-ui/core';
import Chart from "./Measurements/Chart";
import LoadMeasurements from "./Measurements/LoadMeasurements";
import FurfuralMeasurements from "./Measurements/FurfuralMeasurements"
import OilQualityMeasurements from "./Measurements/OilQualityMeasurements"
import DissolvedGasesMeasurements from "./Measurements/DissolvedGasesMeasurements"

export default class TransformerPage extends Component {
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
                return response.json();
          })
          .then( (obj) => {
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
            return (
                <div>
                    <h3>Load Measurements</h3>
                    <LoadMeasurements loadData={this.state.measurements.load}/>
                    <h3>Furfural Measurements</h3>
                    <FurfuralMeasurements furfuralData={this.state.measurements.furfural}/>
                    <h3>Oil Quality Measurements</h3>
                    <OilQualityMeasurements oilQualityData={this.state.measurements.oil_quality}/>
                    <h3>Dissolved Gases</h3>
                    <DissolvedGasesMeasurements measurements={this.state.measurements.dissolved_gases}/>
                </div>
            );
        }
        return <h1>TransformerPage</h1>;
    }
}
