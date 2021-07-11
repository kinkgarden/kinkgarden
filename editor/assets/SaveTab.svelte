<script>
    import Cookies from "js-cookie";
    import { columns, customData } from "./index.js";

    export let saveFormAction;
    export let fetchKink;
    export let patreonClientId;
    export let patreonOk;
    export let patreonError;
    export let listId;

    function submitForm(event) {
        const form = event.currentTarget;

        // we need to put the custom data back into the columns array.
        let submitColumns = $columns.map(({ name, kinks }) => ({
            name,
            kinks: kinks.map((kink) => {
                if (kink.custom) {
                    return fetchKink(kink, $customData);
                } else {
                    return { ...kink };
                }
            }),
        }));

        form.elements["kink-list-data"].value = JSON.stringify(submitColumns);
        form.elements["csrfmiddlewaretoken"].value = Cookies.get("csrftoken");
    }

    let isNew;
    $: isNew = saveFormAction === "";

    let clearEditPassword = false;
    let redirectUrl = window.location.origin + "/patreon/redirect";
</script>

<style>
    form {
        overflow-y: auto;
    }

    fieldset {
        border: 1px solid currentColor;
    }
</style>

<form method="post" action={saveFormAction} on:submit={submitForm}>
    <input type="hidden" name="kink-list-data" value="" />
    <input type="hidden" name="csrfmiddlewaretoken" value="" />
    <fieldset>
        <label>
            View Password
            <input type="password" name="view-password" />
        </label>
        <p>
            If set, will require anyone who wants to view this kink list to
            first enter this password, even if they have the URL. For the truly
            secretive.
            {#if !isNew}Leave blank to keep the previous password.{/if}
        </p>
        {#if !isNew}
            <label>
                Clear view password, if one was set:
                <input type="checkbox" name="clear-view-password" />
            </label>
        {/if}
    </fieldset>
    <fieldset>
        <label>
            Edit Password
            <input
                type="password"
                name="edit-password"
                required={isNew && !clearEditPassword} />
        </label>
        <p>
            If set, will let you come back and use the same password to edit the
            list without making a new one.
            {#if !isNew}Leave blank to keep the previous password.{/if}
        </p>
        <label>
            {#if isNew}
                You probably want to set an edit password, so you can come back
                later and edit this list. If you're absolutely certain you don't
                want to be able to edit this list later, check this box:
            {:else}
                Clear edit password (will make this list impossible to edit):
            {/if}
            <input
                type="checkbox"
                name="clear-edit-password"
                bind:checked={clearEditPassword} />
        </label>
    </fieldset>
    {#if !isNew}
        <fieldset>
            <label>
                Short Link
                {#if patreonOk}
                    <input type="text" name="short-link" />
                {:else if patreonError}error: {patreonError}.{/if}
            </label>
            <p>
                Pledge to
                <a href="https://www.patreon.com/boringcactus">
                    boringcactus's Patreon
                </a>
                at the $5/month tier and then
                <a
                    href="https://www.patreon.com/oauth2/authorize?response_type=code&client_id={patreonClientId}&redirect_uri={redirectUrl}&scope=identity&state={listId}">
                    Log In with Patreon (will lose unsaved changes)
                </a>
                to set a short link for your kink list. For example, you could
                set the short link to
                <code>cutefox</code>
                to have your kink list accessible at
                <code>kink.garden/cutefox</code>
                .
            </p>
            <label>
                Clear short link, if one was set:
                <input type="checkbox" name="clear-short-link" />
            </label>
        </fieldset>
    {/if}
    <input type="submit" value="Save" />
</form>
