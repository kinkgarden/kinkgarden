<script>
    import Cookies from "js-cookie";
    import { columns, customData } from "./index.js";

    export let saveFormAction;
    export let fetchKink;

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
</script>

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
    <input type="submit" value="Save" />
</form>
