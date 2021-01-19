import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

import {makeStyles} from '@material-ui/core/styles';
import List from '@material-ui/core/List'; 
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText'
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Card from '@material-ui/core/Card';


const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
        maxWidth: 500,
        margin: 'auto',
    },
    typography: {
        textAlign: 'center',
        marginTop: 50,
    },
    listCard: {
        marginTop: 5
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
        <div className={classes.root}>
            <Typography variant="h4" className={classes.typography}>
                Transformers
            </Typography>
            <Paper>
                <List className={classes.list}>
                    {transformerList.map(obj => {
                        return (
                            <Card className={classes.listCard}>
                                <ListItem 
                                button 
                                onClick={(e) => clickHandler(e)} 
                                key={obj.id_transformer}
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
            </Paper>
        </div>
    )
}