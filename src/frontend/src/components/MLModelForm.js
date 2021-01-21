import {useState} from 'react'

import Grid from '@material-ui/core/Grid'
import {Alert, AlertTitle} from '@material-ui/lab'
import TextField from '@material-ui/core/TextField'
import Typography from '@material-ui/core/Typography'
import Button from '@material-ui/core/Button'
import {makeStyles} from '@material-ui/core'


const useStyles = makeStyles({
    root: {
        width:'100%',
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
        fontWeight: 'bold',
        marginTop: 20,
        width: '50%'
    }, 
    alert: {
        marginTop: 20
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

    const [submitted, setSubmitted] = useState(false);
    const [trained, setTrained] = useState(false);
    const [errorOccurred, setErrorOccurred] = useState(false);
    function handleSubmition(e) {
        e.preventDefault()
        const url = new URL('http://localhost:8000/api/transformers/train_model/'), 
              params = {stepsBackward: 2, stepsForward: 2}
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
        setErrorOccurred(false);
        setSubmitted(true);
        fetch(url, {
            method: 'GET'
        })
        .then((response) => {
            setSubmitted(false);
            setTrained(true);
        })
        .catch(() => {
            setSubmitted(false)
            setErrorOccurred(true)
        })
    }

    return (
        <>
            <form 
            className={classes.root}
            onSubmit={handleSubmition}
            >
                <Typography variant='h4' className={classes.title}>
                    Train the ML Model
                </Typography>
                <Grid container className={classes.gridContainer}>
                    <Grid item xs={6}>
                        <TextField 
                        variant='outlined' 
                        type='number'
                        label='Steps Back'
                        name="stepsBackward"
                        value={values.stepsBackward}
                        onChange={handleChange}
                        />     
                        <TextField 
                        variant='outlined' 
                        type='number'
                        label='Steps Forward'
                        name="stepsForward"
                        value={values.stepsForward}
                        onChange={handleChange}
                        />     
                        <Button 
                        variant='contained' 
                        type='submit'
                        className={classes.submitButton}
                        >
                            Submit
                        </Button>
                    </Grid>
                    <Grid item xs={6}>
                        {submitted && 
                            <Alert 
                            severity='info'
                            className={classes.alert}
                            >
                                <AlertTitle>Info</AlertTitle>
                                Model is currently being trained
                            </Alert>
                        }
                        {trained && 
                            <Alert 
                            severity='success'
                            className={classes.alert}
                            >
                                <AlertTitle>Success</AlertTitle>
                                Model has been trained
                            </Alert>
                        }
                        {errorOccurred && 
                            <Alert 
                            severity='error'
                            className={classes.alert}
                            >
                                <AlertTitle>Error</AlertTitle>
                                Server Error Occurred try again later
                            </Alert>
                        }
                    </Grid>
                </Grid>
            </form>
        </>
    )
}