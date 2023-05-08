import Link from 'next/link';
import Head from 'next/head';
import Layout from '../components/layout';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import styles from '../styles/Headings.module.css';
import { useState } from 'react';
import { useRouter } from 'next/router';

export default function Signup() 
{
    const router = useRouter();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [preferred_start, setStart] = useState(0);
    const [preferred_end, setEnd] = useState(0);
    const [resMsg, setResMsg] = useState('');

    function handleUsernameChange(event)
    {
        setUsername(event.target.value);
    }

    function handlePasswordChange(event)
    {
        setPassword(event.target.value);
    }

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
            const body = JSON.stringify({username, password, preferred_start, preferred_end})

            const res = await fetch("http://localhost:8000/register/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: body
            });

            const data = await res.json();
            
            if (res.status == 200)
            {
                router.push('/login');
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
        // Comes from the Layout component we made
        <Layout>

            <Head>
                <title>Sign Up</title>
            </Head>

            <h1 className={styles.centered}> Sign Up </h1>

            <Box
                className={styles.centerBox}
                component="form"
                sx={{
                    '& > :not(style)': { m: 1, width: '25ch' },
                }}
                noValidate
                autoComplete="off"
            >
                <TextField id="outlined-basic" label="Username" variant="outlined" onChange={handleUsernameChange} />
                <TextField id="outlined-basic" label="Password" variant="outlined" onChange={handlePasswordChange} />
                <TextField id="outlined-basic" label="Preferred Start Time" variant="outlined" onChange={handleStart} />
                <TextField id="outlined-basic" label="Preferred End Time" variant="outlined" onChange={handleEnd} />

   
            </Box>
            <h3>
                <Button className={styles.centerBox} variant="outlined" color="secondary" onClick={handleCall}>
                    Sign Up
                </Button>
                <Link className={styles.centerBox} href='/login'>
                    Have an account already?
                </Link>
            </h3>
            <h4 className={styles.centered}>{resMsg}</h4>
            
        </Layout>
    );
}