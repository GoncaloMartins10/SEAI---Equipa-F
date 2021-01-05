import React, { Component } from 'react';
import {Tabs, Tab   } from '@material-ui/core';
import Chart from "./Chart";
import TabPanel from "./TabPanel";

export default class FurfuralMeasurements extends Component {
    constructor(props) {
        super(props);
        console.log(this.props.furfuralData)
        this.state = {
            furfuralData: this.props.furfuralData,
            tabDisplay: 0
        }
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(e, value) {
        this.setState({
            ...this.state,
            tabDisplay: value
        });
    }

    render() {
        return (
            <div>
                <Tabs 
                    onChange={this.handleChange}
                    value={this.state.tabDisplay}
                    indicatorColor="primary"
                    textColor="primary"
                    fullWidth
                >
                    <Tab 
                        label="quantity" 
                    />
                </Tabs>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={0}
                >
                    <Chart 
                        xaxis={this.state.furfuralData.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.furfuralData.map(obj => obj.quantity),
                            label: "quantity"
                        }}
                    />
                </TabPanel>
            </div>
        );
    }
}