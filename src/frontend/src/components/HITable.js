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
        width: '50%',
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



export default function HITable({data}) {
    const classes = useStyles();
    const [algorithms, setAlgorithms] = useState([])

    useEffect(() => {
        let algo = [{}, {}, {}, {}];
        data.forEach(({datestamp, hi, id_algorithm}, index) => {
            algo[id_algorithm-1].id_algorithm = id_algorithm;
            algo[id_algorithm-1].hi = hi;
            algo[id_algorithm-1].datestamp = datestamp;
        })
        setAlgorithms(algo)
    }, [data, setAlgorithms])

    return (
        <div className={classes.outerContainer}>
            <Typography variant='h5' align='center'>
                Most Recent Health Indices
            </Typography>
            <TableContainer component={Paper} className={classes.tableContainer}>
                <Table className={classes.table}>
                    <TableHead className={classes.tableHead}>
                        <TableRow>
                            {['Algorithm ID', 'Health Index', 'Datestamp'].map((obj, index) => (
                                <TableCell key={index} align='left' className={classes.tableHeadCell}>
                                    {obj}
                                </TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {algorithms.map((hiObject, index) => {
                            return (
                                <TableRow key={index} className={classes.tableBodyRow}>
                                    {Object.keys(hiObject).map((key, idx) => {
                                        return (
                                            <TableCell key={idx} align='left' className={classes.tableBodyCell}>
                                                {hiObject[key]}
                                            </TableCell>
                                        )
                                    })}
                                </TableRow>
                            )
                        })}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>

    )
}