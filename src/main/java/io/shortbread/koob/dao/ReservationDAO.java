package io.shortbread.koob.dao;

import io.shortbread.koob.models.Reservation;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

import java.time.LocalDateTime;

public interface ReservationDAO extends CrudRepository<Reservation, Long> {

    @Query(
            value = "SELECT * FROM reservations WHERE (start_datetime BETWEEN ?1 AND ?2) OR (end_datetime BETWEEN ?1 AND ?2)",
            nativeQuery = true
    )
    Iterable<Reservation> findAllBetween(LocalDateTime dateLowerbound, LocalDateTime dateUpperbound);

    @Query(
            value = "SELECT * FROM reservations WHERE room = ?1 AND end_datetime > ?2 AND start_datetime < ?3",
            countQuery = "SELECT count(1) FROM reservations WHERE room = ?1 AND end_datetime > ?2 AND start_datetime < ?3",
            nativeQuery = true)
    Iterable<Reservation> findOverlappings(int room, LocalDateTime startDateTime, LocalDateTime endDateTime);
}
