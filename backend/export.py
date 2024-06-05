from flask import jsonify, send_file
from io import BytesIO
import pandas as pd
from models import db, User, TimeLog

def setup_export(app):
    @app.route('/api/export', methods=['GET'])
    def export_logs():
        email = request.args.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        logs = TimeLog.query.filter_by(user_id=user.id).all()
        log_data = [{
            'id': log.id,
            'log_type': log.log_type,
            'timestamp': log.timestamp
        } for log in logs]

        df = pd.DataFrame(log_data)
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        return send_file(output, attachment_filename='time_logs.xlsx', as_attachment=True)
