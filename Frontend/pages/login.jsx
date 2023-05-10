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

            const res = await fetch("/signin/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                credentials: 'same-origin',
                body: body
            });

            const data = await res.json();

            if (res.status == 200)
            {
                localStorage.setItem("token", data.token)
                router.push('/')
            }
            else if (res.status == 401)
            {
                setResMsg("Unauthorized")
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
                // className={styles.centerBox}
                style={{"margin-left":50}}
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
                <Link style={{"margin-left":30}} href='/signup'>
                No account yet?
            </Link>
            </Box>
            <h4 className={styles.centered}>{resMsg}</h4>
            

            
            
        </Layout>
    );
}
