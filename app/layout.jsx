import { Footer, Layout, Navbar } from 'nextra-theme-docs'
import { Head } from 'nextra/components'
import { getPageMap } from 'nextra/page-map'
import 'nextra-theme-docs/style.css'

export const metadata = {
    title: {
        default: 'Algorytmy tekstowe',
        template: 'Algorytmy tekstowe | %s'
    },
}

const navbar = <Navbar logo={<b>Algorytmy tekstowe</b>} projectLink="https://github.com/langMonk/text-algorithms-course" />
const footer = (
    <Footer className="flex-col items-center md:items-start">
        Algorytmy tekstowe {new Date().getFullYear()}
    </Footer>
)

export default async function RootLayout({ children }) {
    return (
        <html
            lang="pl"
            dir="ltr"
            suppressHydrationWarning
        >
        <Head>
        </Head>
        <body>
        <Layout
            //banner={banner}
            navbar={navbar}
            pageMap={await getPageMap()}
            docsRepositoryBase="https://github.com/langMonk/text-algorithms-course/tree/main"
            editLink=""
            sidebar={{ defaultMenuCollapseLevel: 1 }}
            footer={footer}
            feedback={{content: 'Zauważyłeś błąd, masz pomysł co poprawić - zgłoś propozycję!'}}
        >
            {children}
        </Layout>
        </body>
        </html>
    )
}