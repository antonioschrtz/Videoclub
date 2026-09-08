from odoo import api, fields, models
from odoo.exceptions import ValidationError


class VideoclubRental(models.Model):
    _name = "videoclub.rental"
    _description = "Rental of a tape"
    _order = "rental_date desc"

    tape_id = fields.Many2one(
        "videoclub.tape", string="Tape", required=True, ondelete="cascade"
    )
    customer_id = fields.Many2one("res.partner", string="Customer", required=True)

    rental_date = fields.Date(
        string="Rental date", default=fields.Date.context_today, required=True
    )
    expected_return_date = fields.Date(string="Expected return date")
    actual_return_date = fields.Date(string="Actual return date")

    state = fields.Selection(
        [("active", "Active"), ("returned", "Returned")],
        string="State",
        default="active",
        required=True,
    )

    @api.constrains("state", "tape_id", "customer_id")
    def _check_rental_limits(self):
        for rental in self:
            if rental.state != "active" or not rental.customer_id or not rental.tape_id:
                continue
            customer = rental.customer_id
            movie = rental.tape_id.movie_id
            active_rentals = self.env["videoclub.rental"].search(
                [("customer_id", "=", customer.id), ("state", "=", "active")]
            )
            if movie and active_rentals.filtered(
                lambda other: other.id != rental.id and other.tape_id.movie_id == movie
            ):
                raise ValidationError(
                    "A client cannot rent two tapes of the same movie at the same time."
                )
            if len(active_rentals) > 3:
                raise ValidationError(
                    "A client cannot rent more than 3 tapes at the same time."
                )
