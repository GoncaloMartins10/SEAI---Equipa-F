import React, { Component } from 'react';

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
                        furfural: obj.furfural,
                        oil_quality: obj.oil_quality,
                        dissolved_gases: obj.dissolved_gases
                    }
                })
          });
    }

    render() {
        if (this.state.measurements) {
            console.log("we are here");
            console.log(this.state.measurements);
        }
        return <p>This is the TransformerPage {this.transformerId}</p>;
    }
}