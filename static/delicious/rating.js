const rate = (rating, pk) => {
    fetch(`/details/${pk}/rate/${rating}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => {
        window.location.reload();
    })
}