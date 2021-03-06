import React from 'react';
import {Line} from "react-chartjs-2";


export default function Chart({xaxis, yaxis, ...other}) {
    if(!xaxis) {
        return <div/>;
    };

    const data = {
        chartData: {
            labels: xaxis,
            datasets: [
                {
                    label: yaxis.label,
                    data: yaxis.data,
                    backgroundColor: 'rgba(222, 163, 35, 0.5)', 
                }
            ]
        }
    };



    return (
        <div style={{height: '90%', width: '90%', margin: 'auto'}}> {
            data ? 
                <Line
                  data={data.chartData}
                  responsive={true}
                  options={{
                      padding: 5,
                      maintainAspectRatio: false,
                      scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                            }
                        }],
                        xAxes: [{
                            type: 'time',
                            time: {
                                unit: 'year',
                                unitStepSize: 1.5
                            }
                        }]
                      }
                  }}
                />
                : null
            }
        </div>
    )
}

