import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import { useState } from 'react';
// import Cookies from 'js-cookie';


export default function Tasks(props)
{
    // const [result, setResult] = useState(props.result);
    const [resMsg, setResMsg] = useState('');

    const handleCall = async() => {
        try {
            const body = JSON.stringify({
              "tasks": props.result
            })
            console.log(body)
            const res = await fetch("http://localhost:8000/confirm/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': "Token " + localStorage.getItem("token")
                },
                credentials: 'same-origin',
                body: body
            });
    
            const data = await res.json();
            
            if (res.status == 200)
            {
                console.log(data);
                setResMsg(data)
            }
            else if (res.status == 401)
            {
                setResMsg("Unauthorized")
            }
            else
            {
                setResMsg(data);
            }
    
        } catch (err) {
            console.error(err);
        }
    }


    function handleEdit()
    {
        return // nothing yet
    }

        return props.result == null ?  (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 50 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Task Name</TableCell>
            <TableCell align="right">Task Length (Hours)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {props.taskItems.map((task) => (
            <TableRow
              key={task.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {task.name}
              </TableCell>
              <TableCell align="right">{task.length}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
            
           
        ) :  (
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 50 }} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>Task Name</TableCell>
                  <TableCell>Start Time</TableCell>
                  <TableCell>End Time</TableCell>
                  <TableCell align="right">Task Length (Hours)</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {props.result.map((task) => (
                  <TableRow
                    key={task.name}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                  >
                    <TableCell component="th" scope="row">
                      {task.name}
                    </TableCell>
                    <TableCell component="th" scope="row">
                      {task.start}
                    </TableCell>
                    <TableCell component="th" scope="row">
                      {task.end}
                    </TableCell>
                    <TableCell align="right">{task.length}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            <Button variant="contained" color="primary" onClick={handleCall} >Confirm</Button>
            <Button style={{margin:20}} variant="contained" color="primary" onClick={handleEdit} >Edit</Button>
            <h4>{resMsg}</h4>
            
        </TableContainer>
        );
    
}