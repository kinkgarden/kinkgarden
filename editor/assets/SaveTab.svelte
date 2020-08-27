<script>
    import Cookies from "js-cookie";
    import { columns } from "./index.js";

    export let saveFormAction;

    function submitForm(event) {
        const form = event.currentTarget;
        form.elements["kink-list-data"].value = JSON.stringify($columns);
        form.elements["csrfmiddlewaretoken"].value = Cookies.get("csrftoken");
    }

    let isNew;
    $: isNew = saveFormAction === "";
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
    </fieldset>
    <fieldset>
        <label>
            Edit Password
            <input type="password" name="edit-password" />
        </label>
        <p>
            If set, will let you come back and use the same password to edit the
            list without making a new one.
            {#if !isNew}Leave blank to keep the previous password.{/if}
        </p>
    </fieldset>
    <input type="submit" value="Save" />
</form>
