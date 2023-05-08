// wraps all the pages in the application. 

import '../styles/globals.css'

export default function App({ Component, pageProps })
{
    return <Component {...pageProps} />;
}