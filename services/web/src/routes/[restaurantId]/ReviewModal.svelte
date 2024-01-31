<script lang="ts">
  let stars = 0;
  let description = '';
  export let showModal = false;
  export let handleSubmit = (stars: number, description: string) => {};

  function handleClose() {
    showModal = false;
  }
</script>

<div class="modal">
  <div class="modal-content">
    <button class="close-button" on:click={handleClose}>X</button>
    <h2>Create Review</h2>
    <form on:submit|preventDefault={() => handleSubmit(stars, description)}>
      <div class="form-group">
        <label for="stars">Stars:</label>
        <input type="number" id="stars" min="1" max="5" bind:value={stars} required />
      </div>

      <label for="description">Description:</label>
      <div class="form-group">
        <textarea id="description" rows="3" bind:value={description} required></textarea>
      </div>

      <div class="submit-button-container">
        <button type="submit">Submit</button>
      </div>
    </form>
  </div>
</div>

<style>
  .modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    border-radius: 10px;
    z-index: 9999;
    width: 33vw;
    height: 33vh;
    background-color: #444;
    color: #fff;
  }

  .modal-content {
    position: relative;
    padding: 20px;
  }

  .close-button {
    position: absolute;
    right: 10px;
    top: 10px;
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }

  .form-group {
    margin-bottom: 20px;
  }

  .submit-button-container {
    display: flex;
    justify-content: flex-end;
  }

  textarea {
    width: 100%;
    box-sizing: border-box;
  }
</style>
