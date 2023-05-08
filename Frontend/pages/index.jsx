import Head from 'next/head';
import Layout, { siteTitle } from '../components/layout';
import utilStyles from '../styles/utils.module.css';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import styles from '../styles/Headings.module.css';
import { useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';


export default function Home() 
{
  const router = useRouter();

  const [resMsg, setResMsg] = useState('');
  const [name, setName] = useState('');
  const [length, setLength] = useState('');
  const [taskItems, setTaskItems] = useState([]);

  function handleLength(event)
  {
    setLength(event.target.value);
  }

  function handleName(event)
  {
    setName(event.target.value);
  }

  function handleTask(event)
  {
    setTaskItems([...taskItems, {
    "name": name,
    "length": length
    }])
  }

  const handleCall = async() => {
    try {
        const body = JSON.stringify({
          "user": localStorage.getItem('username'),
          "tasks": taskItems
        })
        console.log(body)
        const res = await fetch("http://localhost:8000/schedule/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: body
        });

        const data = await res.json();
        
        if (res.status == 200)
        {
            console.log(data);
            setTaskItems([]);
        }
        else
        {
            setResMsg(data);
        }

    } catch (err) {
        console.error(err);
    }
}
  return (
    <Layout home>
      <Head>
        <title>{siteTitle}</title>
      </Head>
      
      <section className={utilStyles.headingMd}>
        <h1 className={styles.centered}>Add tasks that must be completed in the next 7 days</h1>

        <Box
                className={styles.centerBox}
                component="form"
                sx={{
                    '& > :not(style)': { m: 1, width: '25ch' },
                }}
                noValidate
                autoComplete="off"
            >
                <TextField id="outlined-basic" label="Task Name" variant="outlined" onChange={handleName} />
                <TextField id="outlined-basic" label="Task Length (1 to 23 hours)" variant="outlined" onChange={handleLength} />
                <h3>
                  <Button className={styles.centerBox} variant="outlined" color="secondary" onClick={handleTask}>
                      Add task
                  </Button>
                  <Button variant="outlined" color="secondary" onClick={handleCall} >Find me a schedule</Button>
                </h3>
                <Link className={styles.hyperlink} href='/settings'>
          Settings
        </Link>
        <h4 className={styles.centered}>{resMsg}</h4>
        </Box>
        <ul>
          {taskItems.map((task) => <li key={task.name}><p>{task.name}</p><span>{task.length}</span></li>)}
        </ul>
    


      </section>
    </Layout>
  )
}