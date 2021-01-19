import React from 'react';

/*export default class TabPanel extends Component {
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
}*/



function TabPanel({children, value, index, ...other}) {
    return (
        <div
          hidden={value !== index}
          id={`scrollable-tabpanel-${index}`}
          {...other}
          style={{
              marginTop: 5,
              width: '100%', 
              height: '80%',
          }}
        >
            {value === index && children}
        </div>
    )
}

export default TabPanel;