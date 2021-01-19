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
        <div style={{height: '100%'}}> {
            data ? 
                <Line
                  data={data.chartData}
                  options={{
                      padding: 5,
                      maintainAspectRatio: false,
                  }}
                />
                : null
            }
        </div> 
    );
}

