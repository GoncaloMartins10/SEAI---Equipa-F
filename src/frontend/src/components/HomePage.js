import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

import {makeStyles} from '@material-ui/core/styles';
import List from '@material-ui/core/List'; 
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText'
import Typography from '@material-ui/core/Typography';


const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
        maxWidth: 500,
        backgroundColor: theme.palette.background.paper,
        margin: 'auto',
    },
    typography: {
        textAlign: 'center',
    },
    list: {
        border: '1px solid',
        padding: 0 
    },
    listItem: {
        borderBottom: '1px solid'
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
            <List className={classes.list}>
                {transformerList.map(obj => {
                    return (
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
                    );
                })}
            </List>
        </div>
    )
}