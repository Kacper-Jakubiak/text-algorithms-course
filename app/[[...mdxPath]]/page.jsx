import {generateStaticParamsFor, importPage} from 'nextra/pages'
import {useMDXComponents} from "nextra-theme-docs";

export const generateStaticParams = generateStaticParamsFor('mdxPath')

export async function generateMetadata(props) {
    const params = await props.params
    const {metadata} = await importPage(params.mdxPath)
    return metadata
}

const Wrapper = useMDXComponents().wrapper

export default async function Page(props) {
    const params = await props.params
    const result = await importPage(params.mdxPath)
    const {default: MDXContent, toc, metadata} = result
    return (
        <Wrapper toc={toc} metadata={metadata}>
            <MDXContent {...props} params={params}/>
        </Wrapper>
    )
}