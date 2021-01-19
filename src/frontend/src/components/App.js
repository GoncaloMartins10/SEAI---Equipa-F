import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import HomePage from "./HomePage";
import TransformerPage from "./TransformerPage";


export default function App() {
    return ( 
        <Router>
            <Switch>
                <Route exact path='/' component={HomePage} />
                <Route path='/transformer/:transformerId' component={TransformerPage} />
            </Switch>
        </Router>
    );
}