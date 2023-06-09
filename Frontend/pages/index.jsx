import Head from 'next/head';
import Layout, { siteTitle } from '../components/layout';
import utilStyles from '../styles/utils.module.css';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import styles from '../styles/Headings.module.css';
import { useState, useEffect } from 'react';
import Tasks from '../components/Tasks';
import Link from 'next/link';

export default function Home() 
{
  const [resMsg, setResMsg] = useState('');
  const [name, setName] = useState('');
  const [length, setLength] = useState('');
  const [taskItems, setTaskItems] = useState([]);
  const [result, setResult] = useState(null);
  const [content, setContent] = useState(<></>);

  function handleLength(event)
  {
    setLength(event.target.value);
  }

  function handleName(event)
  {
    setName(event.target.value);
  }

  function handleTask()
  {
    setTaskItems([...taskItems, {
    "name": name,
    "length": length
    }])
    console.log(taskItems)
  }
  
  const handleCall = async() => {
    try {
        const body = JSON.stringify({
          "tasks": taskItems
        })
        console.log(body)
        const res = await fetch("/schedule/", {
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
            setTaskItems([]);
            setResult(data.tasks);
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

  useEffect(() =>
  {
    if (localStorage.getItem("token") != null)
    {
      setContent(
        <Layout home>
        <Head>
          <title>{siteTitle}</title>
        </Head>
        <section className={utilStyles.headingMd}>
          <h1 className={styles.centered}>Add tasks that must be completed in the next 7 days</h1>
          <p style={{"text-align":"center"}} className={styles.centered}>{resMsg}</p>
          <Box
                  className={styles.centered}
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
                    <Button style={{"margin-right":30}} variant="outlined" color="secondary" onClick={handleTask}>
                        Add task
                    </Button>
                    <Button className={styles.centered} variant="outlined" color="secondary" onClick={handleCall} >Find me a schedule</Button>
                  </h3>
         
          </Box>
  
          <div>
            <Tasks result={result} taskItems={taskItems} />
          </div>
        </section>
      </Layout>
      )
    } else
    {
      setContent(
        <>
          <p>You need an account to access this page, please log in...</p>
          <Link href='/login'>Log in</Link>
        </>
      )
    }
  }, [name, length, taskItems, result, resMsg])

  return content;
}