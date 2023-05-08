import Link from 'next/link';
import Head from 'next/head';
import Layout from '../components/layout';
import styles from '../styles/Headings.module.css';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { useState } from 'react';
import Button from '@mui/material/Button';
import { useRouter } from 'next/router'

export default function Settings() 
{
    const router = useRouter();
    const [preferred_start, setStart] = useState('');
    const [preferred_end, setEnd] = useState('');
    const [resMsg, setResMsg] = useState('');
    const username = localStorage.getItem('username');

    function handleStart(event)
    {
        setStart(parseInt(event.target.value));
    }

    function handleEnd(event)
    {
        setEnd(parseInt(event.target.value));
    }

    const handleCall = async() => {
        try {
            const body = JSON.stringify({username, preferred_start, preferred_end})

            const res = await fetch("http://localhost:8000/update/", {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: body
            });

            const data = await res.json();
            
            if (res.status == 200)
            {
                router.push('/');
            }
            else
            {
                console.log(data)
                setResMsg(data);
            }
        } catch (err) {
            console.error(err);
        }
    }

    return (
        // Comes from the Layout component we made
        <Layout>

            <Head>
                <title>Settings</title>
            </Head>
            <h1 className={styles.centered}> Settings </h1>

            <Box className={styles.centered}>
            <p>
                <TextField style = {{width: 275}} id="outlined-basic" label="Updated Preferred Start Time" variant="outlined" onChange={handleStart} />
            </p>
                <TextField style = {{width: 275}} id="outlined-basic" label="Updated Preferred End Time" variant="outlined" onChange={handleEnd} />
            <p>
                <Button className={styles.centerBox} variant="outlined" color="secondary" onClick={handleCall}>
                    Update Preferences
                </Button>
            </p>
            </Box>  
            <h2 className={styles.centered} >
                <Link href="/">Back to Home</Link>
            </h2>

            <h4 className={styles.centered}>{resMsg}</h4>
        </Layout>
    );
}