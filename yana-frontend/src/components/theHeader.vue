<template>
    <header>
        <nav>
            <ul>
                <li><router-link to="/">Main Page</router-link></li>
                <li><router-link to="/newsrefresher">Trigger News Article Refresh</router-link></li>
                <li>Number of Processed articles : {{ $store.getters.NumberOfArticles }}</li>
            </ul>
        </nav>
    </header>
</template>

<script>
export default {

}
</script>
<style scoped>

header {
    display:flex;
    background-color: #977325;
    align-items: center;
}

ul {
    list-style:none;
    margin:0;
    padding:0;
}

li {
    border-radius: 10%;
    text-align: center;
    vertical-align: center;
}

a{
    text-decoration:none;
border-color:#45006d;
}

a:hover,
a:active,
a.router-link-active{
    border-color: #580986;
}
</style>
