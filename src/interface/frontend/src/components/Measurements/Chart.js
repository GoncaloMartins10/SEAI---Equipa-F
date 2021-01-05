import React, { Component } from 'react';
import {Tabs, Tab   } from '@material-ui/core';
import Grid from "@material-ui/core/Grid";
import {Line, Bar} from "react-chartjs-2";


export default class Chart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            chartData: {
                labels: this.props.xaxis,
                datasets: [
                    {
                        label: this.props.yaxis.label,
                        data: this.props.yaxis.data
                    }
                ]
            }
        };
    }
    render() {
        return (
            <div className='chart'>
                <Line
                data={this.state.chartData}
                options={{
                    maintainAspectRatio: false
                }}
                />
            </div>
        );
    }
}