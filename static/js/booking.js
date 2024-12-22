function openEditModal(bookingId, isStarted, isCompleted) {
    $('#editModal').modal('show');
    isStarted = (isStarted === 'True');
    isCompleted = (isCompleted === 'True');

    const bookingCompletedMessage = document.getElementById('bookingCompletedMessage');
    if (!isStarted) {
        console.log('booking not started');
        bookingCompletedMessage.style.display = 'none';
        document.getElementById('completeBooking').disabled = true;
        document.getElementById('startBooking').disabled = false;
        document.getElementById('startBooking').onclick = () => {
            fetch(`/updateBooking/${bookingId}?action=start`, {
                method: 'POST'
            })
            .then(response => response.text())
            .then(data => {
                alert('Booking started successfully!');
                $('#editModal').modal('hide');
                location.reload();
            })
            .catch(error => console.error('Error:', error));
        };
    } else if (!isCompleted) {
        bookingCompletedMessage.style.display = 'none';
        document.getElementById('startBooking').disabled = true;
        document.getElementById('completeBooking').disabled = false;
        document.getElementById('completeBooking').onclick = () => {
            fetch(`/updateBooking/${bookingId}?action=complete`, {
                method: 'POST'
            })
            .then(response => response.text())
            .then(data => {
                alert('Booking completed successfully!');
                $('#editModal').modal('hide');
                location.reload();
            })
            .catch(error => console.error('Error:', error));
        };
    } else {
        document.getElementById('startBooking').disabled = true;
        document.getElementById('completeBooking').disabled = true;
        bookingCompletedMessage.style.display = 'block';
    }
}