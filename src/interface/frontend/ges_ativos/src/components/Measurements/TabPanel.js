import React, { Component } from 'react';

export default class TabPanel extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                {this.props.value === this.props.index ? this.props.children : null} 
            </div>
        );
    }
}