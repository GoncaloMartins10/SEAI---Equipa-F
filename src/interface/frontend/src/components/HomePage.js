import React, { Component } from 'react';
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import { withRouter } from "react-router-dom";


export default class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            transformers: null
        };
        this.handleClick = this.handleClick.bind(this);
    }
    componentDidMount() {
        this.transformersGet();
    }

    transformersGet() {
        fetch('/api/transformers/', {
            method: "GET"
        })
        .then((response) => response.json())
        .then((obj) => {
            this.setState({
                transformers: obj.transformers
            });
        })
    }

    handleClick(e) {
        this.props.history.push("/transformer/" + e.target.innerText);
    }

    render() {
        if (!this.state.transformers) {
            return <div />
        }
        return(
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Typography variant="h4" component="h4">
                        Transformers
                    </Typography>
                </Grid>
                <Grid item xs={6} align="center">
                    <List>
                        {this.state.transformers.map(obj => {
                            return (
                                <ListItem button onClick={this.handleClick} >
                                    <ListItemText primary={obj.id_transformer} />
                                </ListItem>
                                
                            );
                        })}
                    </List>
                </Grid>
            </Grid>
        );
    }
}