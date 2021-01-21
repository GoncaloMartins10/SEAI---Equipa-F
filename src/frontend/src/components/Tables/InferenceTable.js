import React, {useState, useEffect} from 'react'

import {makeStyles} from '@material-ui/core'
import Typography from '@material-ui/core/Typography'
import TableContainer from '@material-ui/core/TableContainer'
import Table from '@material-ui/core/Table'
import TableHead from '@material-ui/core/TableHead'
import TableBody from '@material-ui/core/TableBody'
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'
import Paper from '@material-ui/core/Paper'



const useStyles = makeStyles({
    outerContainer: {
        boxSizing: 'border-box',
        marginTop: 30,
        paddingLeft: 10, 
        width: '100%',
    },
    tableContainer: {
        marginTop: 53
    },
    table: {

    },
    tableHead: {
        backgroundColor: 'rgba(0,0,0,1)',
        color: 'rgba(255,255,255,1)',
        borderRadius: 4
    },
    tableHeadCell: {
        color: 'rgba(255,255,255,1)',
        fontSize: 14,
        fontWeight: 'bold',
    },
    tableBodyRow: {
        '&:nth-of-type(odd)': {
            backgroundColor: 'rgba(190,190,190,0.3)'
        }
    }
});



export default function InferenceTable({data, transformerId}) {
    const classes = useStyles();

    return (
        <div className={classes.outerContainer}>
            <Typography variant='h5' align='center'>
                Transformer Inferred State
            </Typography>
            <TableContainer component={Paper} className={classes.tableContainer}>
                <Table className={classes.table}>
                    <TableHead className={classes.tableHead}>
                        <TableRow>
                            {['Year', 'Inferred Health Index'].map((obj, index) => (
                                <TableCell key={index} align='left' className={classes.tableHeadCell}>
                                    {obj}
                                </TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {Object.keys(data).map((key, index) => {
                            return (
                                <TableRow key={index} className={classes.tableBodyRow}>
                                    <TableCell align='left'>
                                        {key}
                                    </TableCell>
                                    <TableCell align='left'>
                                        {data[key]}
                                    </TableCell>
                                </TableRow>
                            )
                        })}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>

    )
}