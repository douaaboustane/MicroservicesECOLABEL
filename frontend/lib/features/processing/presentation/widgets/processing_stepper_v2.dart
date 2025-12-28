import 'package:flutter/material.dart';
import 'dart:math' as math;
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../data/datasources/job_polling_ds.dart' show JobStatus;

/// Stepper amélioré style "Subway Map" avec ligne ondulée
class ProcessingStepperV2 extends StatelessWidget {
  final JobStatus currentStatus;

  const ProcessingStepperV2({
    super.key,
    required this.currentStatus,
  });

  @override
  Widget build(BuildContext context) {
    final steps = [
      _StepData(
        icon: Icons.search,
        title: EcoStrings.stepOcr,
        description: EcoStrings.stepOcrDesc,
        status: _getStepStatus(JobStatus.ocr),
        color: EcoColors.primaryGreen,
      ),
      _StepData(
        icon: Icons.psychology,
        title: EcoStrings.stepNlp,
        description: EcoStrings.stepNlpDesc,
        status: _getStepStatus(JobStatus.nlp),
        color: EcoColors.scientificBlue,
      ),
      _StepData(
        icon: Icons.recycling,
        title: EcoStrings.stepAcv,
        description: EcoStrings.stepAcvDesc,
        status: _getStepStatus(JobStatus.acv),
        color: EcoColors.lightGreen,
      ),
      _StepData(
        icon: Icons.star,
        title: EcoStrings.stepScore,
        description: EcoStrings.stepScoreDesc,
        status: _getStepStatus(JobStatus.score),
        color: EcoColors.scoreA,
      ),
    ];

    return CustomPaint(
      painter: _SubwayMapPainter(
        steps: steps,
        currentStatus: currentStatus,
      ),
      child: Column(
        children: steps.asMap().entries.map((entry) {
          final index = entry.key;
          final step = entry.value;
          return _buildStep(step, index == steps.length - 1);
        }).toList(),
      ),
    );
  }

  _StepStatus _getStepStatus(JobStatus stepStatus) {
    if (currentStatus == stepStatus) {
      return _StepStatus.inProgress;
    } else if (_isStepCompleted(stepStatus)) {
      return _StepStatus.completed;
    } else {
      return _StepStatus.pending;
    }
  }

  bool _isStepCompleted(JobStatus stepStatus) {
    final order = [
      JobStatus.ocr,
      JobStatus.nlp,
      JobStatus.acv,
      JobStatus.score,
    ];
    final currentIndex = order.indexOf(currentStatus);
    final stepIndex = order.indexOf(stepStatus);
    return currentIndex > stepIndex || currentStatus == JobStatus.done;
  }

  Widget _buildStep(_StepData step, bool isLast) {
    return Padding(
      padding: const EdgeInsets.only(left: 8, right: 16, bottom: 32),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Icône avec ligne
          Column(
            children: [
              _buildStepIcon(step),
              if (!isLast)
                Container(
                  width: 2,
                  height: 60,
                  color: step.status == _StepStatus.completed
                      ? step.color
                      : Colors.grey[300],
                ),
            ],
          ),
          const SizedBox(width: 16),
          // Contenu
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  step.title,
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: step.status == _StepStatus.completed
                        ? step.color
                        : step.status == _StepStatus.inProgress
                            ? step.color
                            : Colors.grey[600],
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  step.description,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStepIcon(_StepData step) {
    switch (step.status) {
      case _StepStatus.completed:
        return Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: step.color,
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: step.color.withValues(alpha: 0.4),
                blurRadius: 10,
                spreadRadius: 2,
              ),
            ],
          ),
          child: const Icon(Icons.check, color: Colors.white, size: 24),
        );
      case _StepStatus.inProgress:
        return Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: step.color.withValues(alpha: 0.2),
            shape: BoxShape.circle,
            border: Border.all(color: step.color, width: 3),
          ),
          child: SizedBox(
            width: 24,
            height: 24,
            child: CircularProgressIndicator(
              strokeWidth: 3,
              valueColor: AlwaysStoppedAnimation<Color>(step.color),
            ),
          ),
        );
      case _StepStatus.pending:
        return Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: Colors.grey[200],
            shape: BoxShape.circle,
            border: Border.all(color: Colors.grey[400]!, width: 2),
          ),
          child: Icon(
            step.icon,
            color: Colors.grey[600],
            size: 24,
          ),
        );
    }
  }
}

/// Painter pour la ligne ondulée style subway map
class _SubwayMapPainter extends CustomPainter {
  final List<_StepData> steps;
  final JobStatus currentStatus;

  _SubwayMapPainter({
    required this.steps,
    required this.currentStatus,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3
      ..strokeCap = StrokeCap.round;

    // Dessiner la ligne ondulée entre les étapes
    for (int i = 0; i < steps.length - 1; i++) {
      final currentStep = steps[i];
      final nextStep = steps[i + 1];

      final startY = 24.0 + (i * 80.0); // Position de l'icône
      final endY = 24.0 + ((i + 1) * 80.0);

      final isCompleted = currentStep.status == _StepStatus.completed ||
          currentStep.status == _StepStatus.inProgress;

      paint.color = isCompleted
          ? currentStep.color
          : Colors.grey[300]!;

      // Ligne ondulée
      final path = Path();
      path.moveTo(24, startY);
      
      // Créer une courbe douce
      final controlPoint1 = Offset(24, startY + 20);
      final controlPoint2 = Offset(24, endY - 20);
      path.cubicTo(
        controlPoint1.dx,
        controlPoint1.dy,
        controlPoint2.dx,
        controlPoint2.dy,
        24,
        endY,
      );

      canvas.drawPath(path, paint);
    }
  }

  @override
  bool shouldRepaint(_SubwayMapPainter oldDelegate) =>
      oldDelegate.currentStatus != currentStatus;
}

enum _StepStatus { pending, inProgress, completed }

class _StepData {
  final IconData icon;
  final String title;
  final String description;
  final _StepStatus status;
  final Color color;

  _StepData({
    required this.icon,
    required this.title,
    required this.description,
    required this.status,
    required this.color,
  });
}

