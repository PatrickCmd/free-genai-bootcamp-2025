import React from 'react';
import { Link } from 'react-router-dom';
import { StudyActivity } from '../../types/studyActivities';

interface ActivityCardProps {
  activity: StudyActivity;
}

const ActivityCard: React.FC<ActivityCardProps> = ({ activity }) => {
  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-2">{activity.name}</h2>
      <p className="text-gray-400 mb-4">Group: {activity.group_name}</p>
      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-400">
          Reviews: {activity.review_items_count}
        </div>
        <div className="space-x-2">
          <Link 
            to={`/study_activities/${activity.id}`}
            className="text-blue-400 hover:text-blue-300 px-4 py-2"
          >
            View
          </Link>
          <Link 
            to={`/study_activities/${activity.id}/launch`}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Launch
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ActivityCard; 