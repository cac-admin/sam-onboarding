import Link from 'next/link';
import Head from 'next/head';
import Layout from '../components/layout';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import styles from '../styles/Headings.module.css';

export default function Login() 
{
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
                <TextField id="outlined-basic" label="Username" variant="outlined" />
                <TextField id="outlined-basic" label="Password" variant="outlined" />
            </Box>
            <h3>
                <Link className={styles.centerBox} href='/signup'>
                    No account yet?
                </Link>
            </h3>
            
        </Layout>
    );
}
