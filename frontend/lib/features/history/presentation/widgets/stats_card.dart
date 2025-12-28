import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';

/// Carte de statistiques collapsible pour l'historique
class StatsCard extends StatefulWidget {
  final int scanCount;
  final double averageScore;
  final String averageScoreLetter;
  final double co2Saved;

  const StatsCard({
    super.key,
    required this.scanCount,
    required this.averageScore,
    required this.averageScoreLetter,
    required this.co2Saved,
  });

  @override
  State<StatsCard> createState() => _StatsCardState();
}

class _StatsCardState extends State<StatsCard>
    with SingleTickerProviderStateMixin {
  bool _isExpanded = true;
  late AnimationController _controller;
  late Animation<double> _heightAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
    _heightAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _toggleExpanded() {
    setState(() {
      _isExpanded = !_isExpanded;
      if (_isExpanded) {
        _controller.forward();
      } else {
        _controller.reverse();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Color(0xFFA8D5A8), // Vert clair (même que Scanner)
            Color(0xFF8BC48B), // Vert moyen
          ],
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: EcoColors.primaryGreen.withValues(alpha: 0.2),
            blurRadius: 16,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        children: [
          // Header
          InkWell(
            onTap: _toggleExpanded,
            borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  const Icon(
                    Icons.bar_chart_rounded,
                    color: Colors.white,
                    size: 24,
                  ),
                  const SizedBox(width: 12),
                  const Text(
                    'Vos statistiques',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const Spacer(),
                  AnimatedRotation(
                    turns: _isExpanded ? 0.5 : 0,
                    duration: const Duration(milliseconds: 300),
                    child: const Icon(
                      Icons.keyboard_arrow_down,
                      color: Colors.white,
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Content (collapsible)
          SizeTransition(
            sizeFactor: _heightAnimation,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
              child: Row(
                children: [
                  Expanded(
                    child: _StatColumn(
                      icon: Icons.qr_code_scanner_rounded,
                      value: '${widget.scanCount}',
                      label: 'Scans',
                    ),
                  ),
                  Expanded(
                    child: _StatColumn(
                      icon: Icons.star_rounded,
                      value: '${widget.averageScoreLetter}',
                      subValue: '${widget.averageScore.toStringAsFixed(0)}/100',
                      label: 'Score moyen',
                      color: EcoColors.getScoreColor(widget.averageScoreLetter),
                    ),
                  ),
                  Expanded(
                    child: _StatColumn(
                      icon: Icons.eco_rounded,
                      value: '${widget.co2Saved.toStringAsFixed(1)}kg',
                      label: 'CO₂ évités',
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _StatColumn extends StatelessWidget {
  final IconData icon;
  final String value;
  final String? subValue;
  final String label;
  final Color? color;
  final String? emoji;

  const _StatColumn({
    required this.icon,
    required this.value,
    this.subValue,
    required this.label,
    this.color,
    this.emoji,
  });

  @override
  Widget build(BuildContext context) {
    final statColor = color ?? Colors.white;

    return Column(
      children: [
        Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: Colors.white.withValues(alpha: 0.25),
            shape: BoxShape.circle,
          ),
          child: emoji != null
              ? Center(
                  child: Text(
                    emoji!,
                    style: const TextStyle(fontSize: 22),
                  ),
                )
              : Icon(icon, color: statColor, size: 22),
        ),
        const SizedBox(height: 10),
        Text(
          value,
          style: TextStyle(
            color: statColor,
            fontSize: 20,
            fontWeight: FontWeight.bold,
            shadows: [
              Shadow(
                color: Colors.black.withValues(alpha: 0.1),
                offset: const Offset(0, 1),
                blurRadius: 2,
              ),
            ],
          ),
        ),
        if (subValue != null) ...[
          const SizedBox(height: 2),
          Text(
            subValue!,
            style: TextStyle(
              fontSize: 12,
              color: Colors.white.withValues(alpha: 0.85),
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(
            fontSize: 13,
            color: Colors.white.withValues(alpha: 0.95),
            fontWeight: FontWeight.w500,
          ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }
}

