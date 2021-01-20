import {useState} from 'react'

import Grid from '@material-ui/core/Grid'
import TextField from '@material-ui/core/TextField'
import Typography from '@material-ui/core/Typography'
import Button from '@material-ui/core/Button'
import {makeStyles} from '@material-ui/core'


const useStyles = makeStyles({
    root: {
        marginTop: 50,
        '& .MuiFormControl-root': {
            marginTop: 20,
            width: '80%',
        }
    },
    title: {
        width: '100%',
        textAlign: 'center',
    },
    gridContainer: {
        marginTop: 30,
        position: 'relative',
    },
    submitButton: {
        position: 'absolute',
        fontWeight: 'bold',
        width: '30%',
        bottom: 2,
        margin: 'auto'
    }
});

const defaultFormValues = {
    stepsForward: 2,
    stepsBackward: 2,
}

export default function MLModelForm() {
    const classes = useStyles();
    const [values, setValues] = useState(defaultFormValues);

    function handleChange(e) {
        const {name, value} = e.target
        setValues({
            ...values,
            [name]: value,
        })
    }

    function handleSubmition() {
        console.log("aceder api para o modelo")
    }

    return (
        <form className={classes.root}>
            <Typography variant='h4' className={classes.title}>
                Train the ML Model
            </Typography>
            <Grid container className={classes.gridContainer}>
                <Grid item xs={6}>
                    <TextField 
                      variant='outlined' 
                      label='Steps Back'
                      name="stepsBackward"
                      value={values.stepsBackward}
                      onChange={handleChange}
                    />     
                    <TextField 
                      variant='outlined' 
                      label='Steps Forward'
                      name="stepsForward"
                      value={values.stepsForward}
                      onChange={handleChange}
                    />     
                </Grid>
                <Grid item xs={6}>
                    <Button 
                      variant='contained' 
                      className={classes.submitButton}
                      onClick={handleSubmition}
                    >
                        Submit
                    </Button>
                </Grid>
            </Grid>
        </form>
    )
}