// wraps all the pages in the application. 

import '../styles/globals.css';
import NavBar from '../components/NavBar';

function SafeHydrate({ children }) {
    return (
      <div suppressHydrationWarning>
        {typeof window === 'undefined' ? null : children}
      </div>
    )
  }

export default function App({ Component, pageProps })
{
    return (
        <div>
            <NavBar/>
            <SafeHydrate><Component {...pageProps} /></SafeHydrate>
        </div>
    );
}