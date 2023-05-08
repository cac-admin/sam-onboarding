import Link from 'next/link';
import Head from 'next/head';
import Layout from '../components/layout';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import styles from '../styles/Headings.module.css';
import { useState } from 'react';
import Button from '@mui/material/Button';
import { useRouter } from 'next/router';

export default function Login() 
{
    const router = useRouter();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [resMsg, setResMsg] = useState('');

    function handleUsernameChange(event)
    {
        setUsername(event.target.value);
    }

    function handlePasswordChange(event)
    {
        setPassword(event.target.value);
    }

    const handleCall = async() => {
        try {
            const body = JSON.stringify({username, password})

            const res = await fetch("http://localhost:8000/signin/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: body
            });

            const data = await res.json();

            if (res.status == 200)
            {
                localStorage.setItem('username', username)
                router.push('/')
            }
            else
            {
                setResMsg(data)
            }

            
        } catch (err) {
            console.error(err);
        }
    }

    return (
        // Comes from the Layout component we made
        <Layout>

            <Head>
                <title>Log In</title>
            </Head>

            <h1 className={styles.centered}> Log In </h1>

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
                <Button className={styles.centerBox} variant="outlined" color="secondary" onClick={handleCall}>
                    Sign in
                </Button>
            </Box>
            <h4 className={styles.centered}>{resMsg}</h4>
            <h3>
                <Link className={styles.centerBox} href='/signup'>
                    No account yet?
                </Link>
            </h3>
            
        </Layout>
    );
}