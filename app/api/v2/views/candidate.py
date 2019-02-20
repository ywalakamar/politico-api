from flask import Blueprint, make_response, request, jsonify
from app.api.v2.models.candidate import Candidate
from utils.validations import validate_party_key_pair_values, \
    error, validUrl, check_for_blanks, check_for_non_ints, success
from utils.helpers import admin_required
from utils.validations import validate_login_key_pair_values

candidate = Blueprint('candidate', __name__)


class CandidateEndPoint:
    """Candidate API Endpoints"""

    @candidate.route('/office/<int:office>/register', methods=["POST"])
    @admin_required
    def register(office):
        """ Register candidate endpoint """

        data = request.get_json()

        if check_for_blanks(data):
            return error(400, "{} cannot be blank".format(', '.join(check_for_blanks(data))))

        if check_for_non_ints(data):
            return error(400, "{} must be an integer".format(', '.join(check_for_non_ints(data))))
        
        office = data.get('office')
        party = data.get('party')
        candidate = data.get('candidate')

        if not Candidate().search_office(office):
            return error(400, "Such an office is not available, please confirm again!")

        if not Candidate().search_party(party):
            return error(400, "Such a party is not registered, please confirm again!")

        if Candidate().search(candidate):
            return error(400, "The candidate is already registered!")

        Candidate().register(office, party, candidate)
        Candidate().update(candidate)
        return success(201, "Candidate registration successfull!", Candidate().get(candidate)), 201
