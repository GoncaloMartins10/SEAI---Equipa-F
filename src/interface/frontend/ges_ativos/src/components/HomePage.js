import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import List from '@material-ui/core/List'; 
import ListItem from '@material-ui/core/ListItem';
import Typography from '@material-ui/core/Typography';


export default function HomePage() {

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
        <div>
            <Typography>
                Transformers
            </Typography>
            <List>
                {transformerList.map(obj => {
                    return (
                        <ListItem onClick={(e) => clickHandler(e)} key={obj.id_transformer}>
                            {obj.id_transformer}
                        </ListItem>
                    );
                })}
            </List>
        </div>
    )
}