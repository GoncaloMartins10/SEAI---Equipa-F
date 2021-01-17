import React, { Component } from "react";
import { render } from "react-dom";
import {BrowserRouter as Router, Switch, Route, Link, Redirect} from "react-router-dom";

import HomePage from "./HomePage";
import TransformerPage from "./TransformerPage";

/*export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return ( 
            <Router>
                <Switch>
                    <Route exact path='/' component={HomePage} />
                    <Route path='/transformer/:transformerId' component={TransformerPage} />
                </Switch>
            </Router>
        );
    }
}*/

export function App() {
    return (
        <h1>Estamos aqui boi</h1>
    )
}