import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

import {makeStyles} from '@material-ui/core/styles';
import List from '@material-ui/core/List'; 
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText'
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Card from '@material-ui/core/Card';
import Grid from '@material-ui/core/Grid';

import MLModelForm from './MLModelForm'


const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
        maxWidth: 500,
        margin: 'auto',
    },
    header: {
        width: '100%',
        height: 100,
        textAlign: 'center',
        marginTop: 20,
    },
    typography: {
        textAlign: 'center',
        marginTop: 50,
    },
    listCard: {
        marginTop: 5,
        margin: 'auto',
        width: '50%'
    },
    list: {
        marginTop: 50, 
        padding: 0,
        '&:last-child': {
        }
    },
    listItem: {
    }
}));

export default function HomePage() {
    const classes = useStyles();

    const [transformerList, setTransformerList] = useState([])
    useEffect(() => {
        const url = 'http://localhost:8000/api/transformers/'
        fetch(url, {
            method: "GET"
        })
        .then((response) => response.json())
        .then((obj) => {
            setTransformerList(obj.transformers);
        })
    }, [setTransformerList])
    
    const history = useHistory();
    const clickHandler = (e) => {
        console.log('transformer/' + e.target.innerText);
        history.push('transformer/' + e.target.innerText);
    }

    return (
        <>
            <Typography variant='h2' className={classes.header}>
                Gestão Digital de Ativos
            </Typography>
            <Grid container>
                <Grid item xs={6}>
                    <Typography variant="h4" className={classes.typography}>
                        Transformers
                    </Typography>
                    <List className={classes.list}>
                        {transformerList.map(obj => {
                            return (
                                <Card 
                                  className={classes.listCard}
                                  key={obj.id_transformer}
                                >
                                    <ListItem 
                                    button 
                                    onClick={(e) => clickHandler(e)} 
                                    className={classes.listItem}
                                    >
                                        <ListItemText
                                        primary={obj.id_transformer}
                                        />
                                    </ListItem>
                                </Card>
                            );
                        })}
                    </List>
                </Grid>
                <Grid item xs={6}>
                    <MLModelForm />
                </Grid>
            </Grid>
        </>
    )
}