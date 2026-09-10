import base64
from datetime import timedelta

from odoo import api, fields, models
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderSVG


class VideoclubMovie(models.Model):
    _name = "videoclub.movie"
    _description = "Movie"

    name = fields.Char(string="Title", required=True)
    active = fields.Boolean(default=True)
    image = fields.Binary(string="Image", attachment=True)
    url_trailer = fields.Char(string="Trailer URL")
    qr_trailer = fields.Binary(string="Trailer QR", compute="_compute_qr_image", attachment=True, store=True)
    qr_trailer_filename = fields.Char(string="Trailer QR filename", compute="_compute_qr_image", store=True)
    director_id = fields.Many2one(
        "res.partner", string="Director", domain="[('is_director', '=', True)]"
    )
    director_image = fields.Binary(
        string="Director image", related="director_id.image_1920", readonly=True
    )
    genre_ids = fields.Many2many("videoclub.genre", string="Genres")
    tapes_ids = fields.One2many("videoclub.tape", "movie_id", string="Tapes")

    # Computed fields
    num_tapes = fields.Integer(
        string="Number of tapes", compute="_compute_tape_stats", store=True
    )
    num_available = fields.Integer(
        string="Available tapes", compute="_compute_tape_stats", store=True
    )
    availability_date = fields.Date(
        string="Availability date", compute="_compute_tape_stats", store=True
    )
    has_rented = fields.Boolean(
        string="I have rented it", compute="_compute_is_rented_by_me", store=False
    )
    rent_state = fields.Selection(
        [
            ("rent", "Alquilar"),
            ("return", "Devolver"),
            ("unavailable", "No disponible"),
        ],
        string="Rent action",
        compute="_compute_rent_state",
        store=False,
    )

    @api.depends('url_trailer')
    def _compute_qr_image(self):
        size = 250
        for record in self:
            if record.url_trailer:
                try:
                    # Generación del QR como SVG con reportlab (ya es una
                    # dependencia de Odoo, no se añade ninguna librería nueva).
                    qr_widget = QrCodeWidget(record.url_trailer)
                    x1, y1, x2, y2 = qr_widget.getBounds()
                    qr_width, qr_height = x2 - x1, y2 - y1
 
                    drawing = Drawing(
                        size,
                        size,
                        transform=[size / qr_width, 0, 0, size / qr_height, 0, 0],
                    )
                    drawing.add(qr_widget)
 
                    svg_data = renderSVG.drawToString(drawing).encode()
                    record.qr_trailer = base64.b64encode(svg_data)
                    record.qr_trailer_filename = f"{record.name or 'trailer'}_qr.svg"
                except Exception:
                    record.qr_trailer = False
                    record.qr_trailer_filename = False
            else:
                record.qr_trailer = False
                record.qr_trailer_filename = False

    @api.depends(
        "tapes_ids.state",
        "tapes_ids.rental_ids.state",
        "tapes_ids.rental_ids.expected_return_date",
    )
    def _compute_tape_stats(self):
        today = fields.Date.context_today(self)
        can_read_rentals = self.env.su or self.env.user.has_group(
            "videoclub.group_videoclub_client"
        )
        for movie in self:
            tapes = movie.tapes_ids
            movie.num_tapes = len(tapes)
            movie.num_available = len(
                tapes.filtered(lambda tape: tape.state == "available")
            )

            if movie.num_available > 0:
                movie.availability_date = today
            elif can_read_rentals:
                active_rentals = tapes.rental_ids.filtered(
                    lambda rental: rental.state == "active"
                )
                dates = [
                    date
                    for date in active_rentals.mapped("expected_return_date")
                    if date
                ]
                movie.availability_date = min(dates) if dates else False
            else:
                movie.availability_date = False

    @api.depends("tapes_ids.rental_ids.customer_id", "tapes_ids.rental_ids.state")
    @api.depends_context("uid")
    def _compute_is_rented_by_me(self):
        partner = self.env.user.partner_id
        can_read_rentals = self.env.su or self.env.user.has_group(
            "videoclub.group_videoclub_client"
        )
        for movie in self:
            if not can_read_rentals:
                movie.has_rented = False
                continue
            rentals = movie.tapes_ids.rental_ids.filtered(
                lambda rental: rental.customer_id.id == partner.id
                and rental.state == "active"
            )
            movie.has_rented = bool(rentals)

    @api.depends("has_rented", "num_available")
    @api.depends_context("uid")
    def _compute_rent_state(self):
        # Determines which button to show for the current user.
        for movie in self:
            if movie.has_rented:
                movie.rent_state = "return"
            elif movie.num_available > 0:
                movie.rent_state = "rent"
            else:
                movie.rent_state = "unavailable"

    def action_rent_movie(self):
        # Creates an active rental for an available tape of the current partner.
        partner = self.env.user.partner_id
        rental_date = fields.Date.context_today(self)
        for movie in self:
            tape = movie.tapes_ids.filtered(lambda item: item.state == "available")[
                :1
            ]  # Avoid IndexError if no available tapes
            if not tape:
                continue
            self.env["videoclub.rental"].create(
                {
                    "tape_id": tape.id,
                    "customer_id": partner.id,
                    "rental_date": rental_date,
                    "expected_return_date": rental_date + timedelta(days=7),
                }
            )
            tape.state = "rented"
        return True

    def action_return_movie(self):
        # Closes the active rentals of the current customer for this movie.
        partner = self.env.user.partner_id
        for movie in self:
            active_rentals = movie.tapes_ids.rental_ids.filtered(
                lambda rental: rental.customer_id.id == partner.id
                and rental.state == "active"
            )
            for rental in active_rentals:
                rental.write(
                    {
                        "state": "returned",
                        "actual_return_date": fields.Date.context_today(self),
                    }
                )
                rental.tape_id.state = "available"
        return True

    def action_manage(self):
        # Applies the action directly according to the current rental state.
        self.ensure_one()
        if self.rent_state == "return":
            return self.action_return_movie()
        if self.rent_state == "rent":
            return self.action_rent_movie()
        # Unavailable: nothing to do.
        return True
