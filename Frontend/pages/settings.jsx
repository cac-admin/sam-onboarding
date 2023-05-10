import Link from 'next/link';
import Head from 'next/head';
import Layout from '../components/layout';
import styles from '../styles/Headings.module.css';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { useState, useEffect } from 'react';
import Button from '@mui/material/Button';
import { useRouter } from 'next/router';

export default function Settings() 
{
    const router = useRouter();
    const [preferred_start, setStart] = useState('');
    const [preferred_end, setEnd] = useState('');
    const [resMsg, setResMsg] = useState('');
    const [content, setContent] = useState(<></>)

    function handleStart(event)
    {
        setStart(event.target.value);
    }

    function handleEnd(event)
    {
        setEnd(event.target.value);
    }

    const handleCall = async() => {
        try {
            const body = JSON.stringify({preferred_start, preferred_end})
            console.log(body)
            const res = await fetch("/update/", {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': "Token " + localStorage.getItem("token")
                },
                body: body
            });

            const data = await res.json();
            
            if (res.status == 200)
            {
                router.push('/');
            }
            else if (res.status == 401)
            {
                setResMsg("Unauthorized");
            }
            else
            {
                setResMsg(data);
            }
        } catch (err) {
            console.error(err);
        }
    }

    useEffect (() => 
    {
        if (localStorage.getItem("token") != null)
        {
            setContent(
                <Layout>

                <Head>
                    <title>Settings</title>
                </Head>
                <h1 className={styles.centered}> Settings </h1>
    
                <Box className={styles.centered}>
                <p>
                    <TextField  type="number" style = {{width: 300}} id="outlined-basic" label="Updated Preferred Start Time" variant="outlined" onChange={handleStart} />
                </p>
                    <TextField type="number" style = {{width: 300}} id="outlined-basic" label="Updated Preferred End Time" variant="outlined" onChange={handleEnd} />
                <p>
                    <Button className={styles.centerBox} variant="outlined" color="secondary" onClick={handleCall}>
                        Update Preferences
                    </Button>
                </p>
                </Box>  
                <h2 className={styles.centered} >
                    <Link href="/">Back to Home</Link>
                </h2>
    
                <h4 style={{"text-align":"center"}} className={styles.centered}>{resMsg}</h4>
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
    }, [preferred_start, preferred_end, resMsg])

    return content;
}